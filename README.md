Ard

A multiplayer turn-based strategy game written from scratch.

For some information and screenshots check out the [website](http://ardthegame.com)

The Game Engine written in C with embedded Python, OpenGL, FreeType, libpng, and SDL for game client.

If you'd like to fork this code and turn it into an open-source game engine, please contact me, I will attach a friendly license.

All rendering in handled by OpenGL and I/O by SDL(Simple DirectMedia Layer), FreeType(TrueType fonts), and libpng.

Game logic is written in python and state only moves between C and Python when the user make some action, allowing the library to keep a high FPS while also allowing the game developer to write Game Logic in a high-level language.

One downside of the approach is that you must manually manage references to Python objects in C for the Python Garbage Collector, but this is quite easy once you see it. Simply pass a pointer to the object to a call to Py_DECREF when you're done with the object. This can be seen frequently in main.c.

There is a server written in TwistedPython which could probably be re-written in a more modern asychronous server such as node.

Features A* algorithm for pathfinding and peer-to-peer network connections which can be run over LAN but can also traverse NAT firewalls by having peers reply to TCP requests which were made to the server, a cute trick which I learned from Skype.

Some game logic is still needed, but the most glaring issue is that the AI hasn't been implemented.

Big thanks to Beej's Guide to Network Programming. https://beej.us/guide/bgnet/




