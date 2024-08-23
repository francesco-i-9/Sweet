"""
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, session, request, redirect, url_for, render_template
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from sqlalchemy import select
import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("dataset/utenti_preferenze.csv")
print(df)

host = "localhost"
username = "root"
password = ""

DATABASE_URL = f"mysql+pymysql://{username}:{password}@{host}/sito"
engine = create_engine(DATABASE_URL)
df.to_sql(name="Preferenze", con=engine, index=False, if_exists="replace")

df=pd.read_csv("preferenze.csv")"""



a={"preferenza":"torta di mele"}

print(a)

    
