# Hotloading Plugins Project
My 'Hotloading Plugins' project consists of the two repositories 'hotloaded-server' and 'hotloaded-plugins'. The project is a test for having a running server that will update a dependency and reload it dynamically without any necessary downtime.

See [Hotloaded Plugins](https://github.com/BVengo/hotloaded-plugins) for the other repository.

## Use-Case
For projects that are dependent on short python scripts which are frequently updated (and need to be immediately deployed), but also need to avoid any downtime. 

Pros:
- No downtime (although a `PLUGINS_UPDATING` flag in the code would be beneficial to temporarily queue up processes)
- Plugins included as a dependency, which means it can be automatically downloaded (and shared dependencies are handled too)
- No need to store both repositories on the server (as would be required for a file-system based setup)
- Make use of source control to track and store plugins code

Cons:
- Unpredictable behaviour if not handled correctly (in-memory objects will still be old)
- Requires two repositories instead of one project that gets re-deployed with a short downtime period


### Other Alternatives
It would be amiss of me to not contemplate other methods of handling this situation as well. The alternative methods I thought of were:

- Reading directly from another project directory, on the same file system
- Storing the scripts in a database, to be dynamically read in

Both of these have similar pros and cons.

Pros:
- Easy to setup

Cons:
- Plugins not listed as a project dependency, despite being one
- Requires additional setup (directory or database setup, having a variable pointing to where it's stored)
- Need to add all plugin dependencies into primary project as well - can be easily missed
