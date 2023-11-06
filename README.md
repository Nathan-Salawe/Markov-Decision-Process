# Markov-Decision-Process
## overview

An application of the markov decision process algorithm.
This project is intended to show the use of markov decision process algorith in it's basic form

the markov decision process algorthm was modified slightly drawing inspiration from the q-learning algorithm to improve performance

## Environment

The environment for this project was created using python's `tkinter` package.
it consists of an MxN grid representing various states.

For this implementation. there have 3 states `open`, `obstacle` and `destination`

## Behaviour
- agent can move into any free state without being penalized
- agent is given `-1` reward everytime it enters into an `obstacle` state
- agent is given `+1` reward when it gets to the `destination` state

## Dependencies

This implementation was done without any third party package or module.

## Running the server
```bash
python3 main.py
```

Choose a grid size and click `start`

click `Go!!` to start exploying the environment 

once the agent is done exploying the environment, you can click on any starting point and the agent will find the shortest route to the destination!.
