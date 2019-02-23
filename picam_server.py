from threading import Thread, Lock
import io
import picamera
from flask import Flask, render_template, Response
import time

app = Flask(__name__)