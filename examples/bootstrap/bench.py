import os
import sys
import time

from pure.compile.Compile import Compile
from pure.component.Registry import Registry
from pure.core.HTML import HTML

from .app.dao.FeaturesDao import content as features_dao_content
from pure.loader import load_module
features_bindings, features_page = load_module(os.path.join(os.path.dirname(__file__), 'views/features_cmp.cmp.py'), 'features_cmp')
from .app.bootstrap import plain


def bench(label, iters, fn):
    fn()
    start = time.perf_counter_ns()
    for _ in range(iters):
        fn()
    per = (time.perf_counter_ns() - start) / iters / 1000

    print("{:<34} {:>8.1f} us/op".format(label, per))

    return per


iters = int(sys.argv[1]) if len(sys.argv) > 1 else 2000

shape_start = time.perf_counter_ns()
unit_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'views', 'features_cmp.py')
page_shape = Registry.unitsFor(unit_file)['Features']['factory']()
Compile.shape(page_shape).compile()
shape_time = (time.perf_counter_ns() - shape_start) / 1000

require_start = time.perf_counter_ns()
renderer = Registry.component(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'views', 'features.pure.py'))
require_time = (time.perf_counter_ns() - require_start) / 1000

first_start = time.perf_counter_ns()
first = features_page()
first_time = (time.perf_counter_ns() - first_start) / 1000

print("page shape + compile: {:.1f} us (once) | artifact require: {:.1f} us (once)".format(shape_time, require_time))
print("page function first render (compiles components): {:.1f} us\n".format(first_time))

plain_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'views', 'features.plain.py')
if os.path.isfile(plain_file):
    os.utime(plain_file, (time.time() - 5, time.time() - 5))

classic = lambda: features_dao_content()

page_time = bench('page function (components + artifact)', iters, lambda: features_page())

bindings = [str(block) for block in features_bindings()]

classic_time = bench('classic build + render', iters, classic)
artifact_time = bench('skeleton artifact + rendered blocks', iters, lambda: renderer.render(bindings))
plain_time = bench('plain view + rendered blocks', iters, lambda: plain('features', bindings))

header = HTML.DOCUMENT_HEADER
document = header + renderer.render(bindings)
print(
    "\npage identical: {} ({} bytes) | page vs classic: {:.2f}x".format(
        'yes' if first == document else 'NO',
        len(first),
        classic_time / page_time
    )
)
print(
    "skeleton identical: {} | {} bytes | artifact vs page: {:.2f}x".format(
        'yes' if renderer.render(bindings) == document[len(header):] else 'NO',
        len(document),
        artifact_time / page_time
    )
)
print(
    "plain identical: {} | plain vs artifact: {:.2f}x".format(
        'yes' if plain('features', bindings) == document else 'NO',
        plain_time / artifact_time
    )
)
