"""
End-to-end test of the component-name rule: run phpstan over a fixture
project that enables only the collectors and UnknownComponentRule, and
read the JSON report.

Skipped when phpstan is not available in the environment.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

PUREPHP_DIR = Path("/home/tintin/codes/purephp")
PHPSTAN_BIN = PUREPHP_DIR / "vendor" / "bin" / "phpstan"


@pytest.mark.skipif(
    not PHPSTAN_BIN.exists(),
    reason="phpstan is not available (run composer install in purephp)",
)
def test_reports_literal_component_names_no_registration_declares(tmp_path):
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()

    (src_dir / "known.cmp.php").write_text(
        """<?php

declare(strict_types=1);

use Pure\\Compile\\Compile;
use Pure\\Component\\Call;
use Pure\\Core\\Slot;

use function Pure\\Component\\{component, register};
use function Pure\\HTML\\span;

function KnownBadge(mixed ...$children): Call
{
    return component(__FUNCTION__, ...$children);
}

register(KnownBadge(...), static fn (): \\Pure\\Compile\\Shape => Compile::shape(
    span(Slot::value('label'))
));
"""
    )

    (src_dir / "static.php").write_text(
        """<?php

declare(strict_types=1);

use Pure\\Compile\\Compile;
use Pure\\Component\\Registry;
use Pure\\Core\\Slot;

use function Pure\\HTML\\span;

Registry::register('StaticBadge', __FILE__, static fn (): \\Pure\\Compile\\Shape => Compile::shape(
    span(Slot::value('label'))
));
"""
    )

    (src_dir / "fcp.cmp.php").write_text(
        """<?php

declare(strict_types=1);

use Pure\\Compile\\Compile;
use Pure\\Component\\Call;
use Pure\\Core\\Slot;

use function Pure\\Component\\{component, register};
use function Pure\\HTML\\span;

function FcBox(mixed ...$children): Call
{
    return component(__FUNCTION__, ...$children);
}

register(FcBox(...), static fn (): \\Pure\\Compile\\Shape => Compile::shape(
    span(Slot::value('label'))
));
"""
    )

    (src_dir / "calls.php").write_text(
        """<?php

declare(strict_types=1);

use Pure\\Component\\Registry;

use function Pure\\Component\\component;

component('KnownBadge');
component('KnownBadg');
component('FcBox');
Registry::component('StaticBadge');
Registry::component('StaticBadg');
"""
    )

    config = tmp_path / "phpstan.neon"
    config.write_text(
        f"""services:
    -
        class: Pure\\StaticAnalysis\\ComponentCallCollector
        tags:
            - phpstan.collector
    -
        class: Pure\\StaticAnalysis\\RegistryCallCollector
        tags:
            - phpstan.collector

rules:
    - Pure\\StaticAnalysis\\UnknownComponentRule

parameters:
    customRulesetUsed: true
    tmpDir: {cache_dir}
"""
    )

    result = subprocess.run(
        [
            sys.executable if False else "php",
            str(PHPSTAN_BIN),
            "analyse",
            "--no-progress",
            "--error-format=json",
            f"--configuration={config}",
            str(src_dir),
        ],
        capture_output=True,
        text=True,
    )

    raw = result.stdout
    brace = raw.find("{")
    assert brace != -1, f"phpstan must print a JSON report: {raw}"
    report = json.loads(raw[brace:])

    assert isinstance(report, dict), f"phpstan must print a JSON report: {raw}"

    messages = []
    for file_data in report.get("files", {}).values():
        for message in file_data.get("messages", []):
            messages.append(message["message"])

    assert result.returncode == 1, "the typo must fail the run"

    for typo in ["KnownBadg", "StaticBadg"]:
        matched = [m for m in messages if f"'{typo}' is not registered" in m]
        assert matched, f"the typo '{typo}' must be reported: {' | '.join(messages)}"

    for known in ["KnownBadge", "StaticBadge", "FcBox"]:
        for message in messages:
            assert f"'{known}' is not registered" not in message
