from .core.SVG import SVG


def a(*args):
    return SVG("a", args)


def animate(*args):
    return SVG("animate", args)


def animatemotion(*args):
    return SVG("animateMotion", args)


globals()["animateMotion"] = animatemotion


def animatetransform(*args):
    return SVG("animateTransform", args)


globals()["animateTransform"] = animatetransform


def circle(*args):
    return SVG("circle", args)


def clippath(*args):
    return SVG("clipPath", args)


globals()["clipPath"] = clippath


def defs(*args):
    return SVG("defs", args)


def desc(*args):
    return SVG("desc", args)


def ellipse(*args):
    return SVG("ellipse", args)


def feblend(*args):
    return SVG("feBlend", args)


globals()["feBlend"] = feblend


def fecolormatrix(*args):
    return SVG("feColorMatrix", args)


globals()["feColorMatrix"] = fecolormatrix


def fecomponenttransfer(*args):
    return SVG("feComponentTransfer", args)


globals()["feComponentTransfer"] = fecomponenttransfer


def fecomposite(*args):
    return SVG("feComposite", args)


globals()["feComposite"] = fecomposite


def feconvolvematrix(*args):
    return SVG("feConvolveMatrix", args)


globals()["feConvolveMatrix"] = feconvolvematrix


def fediffuselighting(*args):
    return SVG("feDiffuseLighting", args)


globals()["feDiffuseLighting"] = fediffuselighting


def fedisplacementmap(*args):
    return SVG("feDisplacementMap", args)


globals()["feDisplacementMap"] = fedisplacementmap


def fedistantlight(*args):
    return SVG("feDistantLight", args)


globals()["feDistantLight"] = fedistantlight


def fedropshadow(*args):
    return SVG("feDropShadow", args)


globals()["feDropShadow"] = fedropshadow


def feflood(*args):
    return SVG("feFlood", args)


globals()["feFlood"] = feflood


def fefunca(*args):
    return SVG("feFuncA", args)


globals()["feFuncA"] = fefunca


def fefuncb(*args):
    return SVG("feFuncB", args)


globals()["feFuncB"] = fefuncb


def fefuncg(*args):
    return SVG("feFuncG", args)


globals()["feFuncG"] = fefuncg


def fefuncr(*args):
    return SVG("feFuncR", args)


globals()["feFuncR"] = fefuncr


def fegaussianblur(*args):
    return SVG("feGaussianBlur", args)


globals()["feGaussianBlur"] = fegaussianblur


def feimage(*args):
    return SVG("feImage", args)


globals()["feImage"] = feimage


def femerge(*args):
    return SVG("feMerge", args)


globals()["feMerge"] = femerge


def femergenode(*args):
    return SVG("feMergeNode", args)


globals()["feMergeNode"] = femergenode


def femorphology(*args):
    return SVG("feMorphology", args)


globals()["feMorphology"] = femorphology


def feoffset(*args):
    return SVG("feOffset", args)


globals()["feOffset"] = feoffset


def fepointlight(*args):
    return SVG("fePointLight", args)


globals()["fePointLight"] = fepointlight


def fespecularlighting(*args):
    return SVG("feSpecularLighting", args)


globals()["feSpecularLighting"] = fespecularlighting


def fespotlight(*args):
    return SVG("feSpotLight", args)


globals()["feSpotLight"] = fespotlight


def fetile(*args):
    return SVG("feTile", args)


globals()["feTile"] = fetile


def feturbulence(*args):
    return SVG("feTurbulence", args)


globals()["feTurbulence"] = feturbulence


def filter(*args):
    return SVG("filter", args)


def foreignobject(*args):
    return SVG("foreignObject", args)


globals()["foreignObject"] = foreignobject


def g(*args):
    return SVG("g", args)


def image(*args):
    return SVG("image", args)


def line(*args):
    return SVG("line", args)


def lineargradient(*args):
    return SVG("linearGradient", args)


globals()["linearGradient"] = lineargradient


def marker(*args):
    return SVG("marker", args)


def mask(*args):
    return SVG("mask", args)


def metadata(*args):
    return SVG("metadata", args)


def mpath(*args):
    return SVG("mpath", args)


def path(*args):
    return SVG("path", args)


def pattern(*args):
    return SVG("pattern", args)


def polygon(*args):
    return SVG("polygon", args)


def polyline(*args):
    return SVG("polyline", args)


def radialgradient(*args):
    return SVG("radialGradient", args)


globals()["radialGradient"] = radialgradient


def rect(*args):
    return SVG("rect", args)


def script(*args):
    return SVG("script", args)


def set(*args):
    return SVG("set", args)


def stop(*args):
    return SVG("stop", args)


def style(*args):
    return SVG("style", args)


def svg(*args):
    return SVG("svg", args)


def switch(*args):
    return SVG("switch", args)


def symbol(*args):
    return SVG("symbol", args)


def text(*args):
    return SVG("text", args)


def textpath(*args):
    return SVG("textPath", args)


globals()["textPath"] = textpath


def title(*args):
    return SVG("title", args)


def tspan(*args):
    return SVG("tspan", args)


def use(*args):
    return SVG("use", args)


def view(*args):
    return SVG("view", args)
