from pure.svg import svg, use

def Icon(icon: str):
    return svg(use().href('#{}'.format(icon)))
