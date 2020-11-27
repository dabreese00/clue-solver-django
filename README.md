# Clueless

Track your [Clue](https://en.wikipedia.org/wiki/Cluedo) games with a convenient web app!

Currently it lets you create and track games.

- User authentication coming soon.
- Better input workflow coming soon.
- Optionally catching your obvious mistakes, coming soon.
- "Cheat mode" coming soon... ;)


## Installing

To-do


## Life's story

This is a project to help teach myself web development.  It's a successor to my
original [Clue Solver in Flask](https://github.com/dabreese00/clue-solver),
created because I wanted to see how using a different set of tools might allow
me to achieve the same ends with more or less ease and elegance.  By contrast
to the original project (which used handwritten classes stored with pickle),
this Django project naturally does use a traditional database backend.

Currently, the frontend is relatively well-developed (around 70-80% of my
initial goal).

As for the backend, so far it's basically just data storage and some limited
validation.  Plans to add a logical inference engine along the lines of the
original project, but this time as a configurable feature at the user's option.
