import time

from visual import JarvisVisual


jarvis = JarvisVisual()

jarvis.show("JARVIS ONLINE")


while jarvis.running:

    jarvis.update()

    time.sleep(0.01)


jarvis.close()