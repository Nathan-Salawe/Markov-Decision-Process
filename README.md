# Markov-Decision-Process
## overview

An application of the markov decision process algorithm.
This project is intended to show the use of markov decision process algorith in it's basic form

the markov decision process algorthm was modified slightly drawing inspiration from the q-learning algorithm to improve performance

## environment

The environment for this project was created using python's `tkinter` package.
it consists of an MxN grid representing various states.

For this implementation. we have 3 states `open`, `obstacle` and `destination`

## Behaviour
- agent can move into any free state without being penalized
- agent is given -1 bonus everytime it enters an `obstacle` state
- agent is given a +1 reward when it gets to the `destination` state

## running the server
```bash
python3 main.py
```
