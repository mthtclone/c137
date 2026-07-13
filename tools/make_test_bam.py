from panda3d.core import CardMaker, NodePath

root = NodePath("test_scene")

cm = CardMaker("test_card")
card = root.attachNewNode(cm.generate())

card.setScale(2)
card.setPos(0, 5, 0)

root.writeBamFile("test_scene.bam")

print("Created test_scene.bam")
