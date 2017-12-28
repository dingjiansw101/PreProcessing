from __future__ import print_function
from pykml.factory import KML_ElementMaker as KML
from lxml import etree

name_object = KML.name("Hello World!")

pml = KML.Placemark(
    KML.name("Hellow World!"),
    KML.Point(
        KML.coordinates("-64.5253, 18.4607")
    )
)

etree.tostring(pml)

print(etree.tostring(pml, pretty_print=True))


