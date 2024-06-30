# Python-Limit-Order-Book

Double Side Limit Order Book implementation in Python, plus webserver, plus command line interface.

# What is it?

This repository consists of the source code for (primarily) two things

- A Limit Order Book implementation, which is wrapped with a FastAPI webserver
- A client CLI which can interact with the webserver

A Limit Order Book is the core piece of infastructure in a financial exchange, such as a stock exchange. They are used to match client buy and sell orders, enabling clients to trade.

# Just show me how to run it

The webserver is running on a Linode. It has the IP address `176.58.122.148 (/24)`. This cloud based VM hosts the FastAPI web API, which provides a REST interface to the Limit Order Book. You can interact with it using the CLI.

## How to use the CLI

The following bash commands show how to run the CLI on Linux. You need to be in the root directory, such that the `limit_order_book_cli` directory is accessable from the current working directory. See the section on Setup Instructions for more information.

```
$ cd Python-Limit-Order-Book
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip3 install -r requirements.txt
$ export PYTHONPATH=`pwd`
$ python3 -m limit_order_book_cli --help
```

#### To send an order to the Limit Order Book:

```
$ python3 -m limit_order_book_cli send-order ORDER_ID TICKER ORDER_SIDE PRICE VOLUME
```

`ORDER_ID` must be a unique order id. There is currently no way to query for a valid order id. It is on my list of things to do. For now, just guess a random value.

`TICKER` can technically be any string, but it is supposed to represent a ticker symbol like `AAPL` or `NVDA`.

`ORDER_SIDE` must be either the string `BUY` or `SELL`.

`PRICE` is an integer price value. It doesn't have any particular meaning since there are no instrument conventions to convert from an integer price scale to a real one in currency units. You can use the `top-of-book` command to find out what current valid top of book prices are, if one exists.

`VOLUME` is an integer number of units.

#### To query the Top Of Book:

```
$ python3 -m limit_order_book_cli top-of-book TICKER
```

`TICKER` can technically be any string, but it is supposed to represent a ticker symbol like `AAPL` or `NVDA`.


# History

The original Limit Order Book was written as part of an interview process, although I happen to have written one previously (in Rust, not Python) during a previous role at a startup Hedge Fund.

- The original interview problem can be found in another repository. (https://github.com/edward-b-1/Python-Limit-Order-Book-Old) There are some issues with this implementation, to be expected as it had to be written quickly.

I realized that there was a more elegant way to write the Limit Order Book implementation, which is why I re-wrote the code. The new version can be found in the `limit_order_book` folder.

# Current State

The Limit Order Book Python package contains a working Limit Order Book implementation, and there are tests for it. The tests are located in the `tests` folder. There are numerous ways in which the Limit Order Book package could be extended and improved. The implementation is quite minimal.

The FastAPI wrapper package contains a minimal code to connect the Limit Order Book up to the internet. It does not have any tests yet. (But probably should.)

The CLI package contains the Command Line Interface which can be used to send messages to the Limit Order Book webserver. The CLI is contained in the folder `limit_order_book_cli`.

The Limit Order Book and Webserver implementations are quite minimal. This isn't designed to be as robust as real production software. You could probably find a way to break it relatively easily. (One obvious example is sending so many orders that the system runs out of memory.) If you do break it, please let me know that it is broken and ideally tell me what you did to break it. That way I can fix it. (But please don't deliberatly run it out of memory as this is an obvious failure mode which I already know about.)

Another fairly obvious shortcoming is that the CLI currently requires the user to supply an Order Id, but it does not provide a way to ask for a valid Order Id. The Order Id shouldn't be something the user has to supply. The Limit Order Book should generate a unique one for every order it receives. I will probably change this if I have time to do so.

# Setup Instructions (detailed)

Change directory to the root directory.

```
$ cd Python-Limit-Order-Book
```

Setup a virtual environment with pip. You will need the appropriate Linux package to be installed for this to work. On Debian based systems `sudo apt install python3.XX-venv` should install it. `3.XX` is the version number. It must match with the output of `python3 --version`.

For example, on my system: `sudo apt install python 3.12-venv`.

To create the virtual environment:

```
$ python3 -m venv .venv
```

Now, activate the virtual environment.

```
$ source .venv/bin/activate
```

Install the Python dependencies.

```
$ pip3 install -r requirements.txt
```

Actually, you can skip the following line. This was needed to get the `uvicorn` webserver to run locally, but you probably don't need it for the CLI.

```
$ export PYTHONPATH=`pwd`
```

Finally, run the CLI and print the help message. You can probably figure out the available options the CLI provides from here.

```
$ python3 -m limit_order_book_cli --help
```
