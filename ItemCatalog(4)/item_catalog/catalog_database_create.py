#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from catalog_database_setup import Base, Category, Item, User
from random import randint

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

user = User(email = "chris22931@gmail.com")
session.add(user)
category = Category(name="Apps & Games")
session.add(category)
item = Item(
    name="Tetris",
    description="Description of Tetris",
    category=category,
    owner=user)
session.add(item)
item = Item(
    name="Minecraft",
    description="Description of Minecraft",
    category=category,
    owner=user)
session.add(item)
item = Item(
    name="Hungry Shark Evolution",
    description="Description of Hungry Shark Evolution",
    category=category,
    owner=user)
session.add(item)
item = Item(
    name="Portal",
    description="Description of Portal",
    category=category,
    owner=user)
session.add(item)
item = Item(
    name="Dota 2",
    description="Description of Dota 2",
    category=category,
    owner=user)
session.add(item)
item = Item(
    name="BioShock",
    description="Description of BioShock",
    category=category,
    owner=user)
session.add(item)
item = Item(
    name="Starcraft",
    description="Description of Starcraft",
    category=category,
    owner=user)
session.add(item)

category = Category(name="Beauty")
session.add(category)
item = Item(
    name="Peel Gel",
    description="Description of Peel Gel",
    category=category,
    owner=user)
session.add(item)
item = Item(
    name="Sunscreen",
    description="Description of Sunscreen",
    category=category,
    owner=user)
session.add(item)
item = Item(
    name="Lip Stick",
    description="Description of Lip stick",
    category=category,
    owner=user)
session.add(item)

category = Category(name="Books")
session.add(category)
item = Item(
    name="Chains of Command",
    description="The assault on Earth was thwarted by the destruction of the "
    "aliens seed ship, but with Mars still under Lanky control, survivors work "
    "frantically to rebuild fighting capacity and shore up planetary defenses. "
    "Platoon sergeant Andrew Grayson must crash-course train new volunteers "
    "all while dulling his searing memories of battle with alcohol and meds.",
    category=category,
    owner=user)
session.add(item)
item = Item(
    name="Wayward",
    description="Welcome to Wayward Pines, population 461. Nestled amid "
    "picture-perfect mountains, the idyllic town is a modern-day Eden... "
    "except for the electrified fence and razor wire, snipers scoping "
    "everything, and the relentless surveillance tracking each word "
    "and gesture.",
    category=category,
    owner=user)
session.add(item)
item = Item(
    name="The Hidden Relic",
    description="With the fate of their homeland still in jeopardy, siblings "
    "Ella and Miro must face the Primates evil as he discovers a new "
    "technique: a method to extract essence from human blood.",
    category=category,
    owner=user)
session.add(item)

category = Category(name="Sports & Outdoors")
session.add(category)
item = Item(
    name="Ball",
    description="Not just a normal ball!",
    category=category,
    owner=user)
session.add(item)
item = Item(
    name="Snowboard",
    description="Really cool Snowboard.",
    category=category,
    owner=user)
session.add(item)
item = Item(
    name="Skateboard",
    description="Skateboard from the Tony Hawk Edition.",
    category=category,
    owner=user)
session.add(item)

category = Category(name="DVD & Blu-ray")
session.add(category)
item = Item(
    name="The Shawshank Redemption",
    description="Two imprisoned men bond over a number of years, "
    "finding solace and eventual redemption through acts of common decency.",
    category=category,
    owner=user)
session.add(item)
item = Item(
    name="The Godfather",
    description="The aging patriarch of an organized crime dynasty transfers "
    "control of his clandestine empire to his reluctant son.",
    category=category,
    owner=user)
session.add(item)
item = Item(
    name="The Dark Knight",
    description="When the menace known as the Joker emerges from his "
    "mysterious past, he wreaks havoc and chaos on the people of Gotham, "
    "the Dark Knight must accept one of the greatest psychological "
    "and physical tests of his ability to fight injustice..",
    category=category,
    owner=user)
session.add(item)

category = Category(name="Watches")
session.add(category)
item = Item(
    name="Ice Watch",
    description="Description of Ice Watch",
    category=category,
    owner=user)
session.add(item)
item = Item(
    name="Casio Digital Watch",
    description="Description of Casio Digital Watch",
    category=category,
    owner=user)
session.add(item)

session.commit()
