"""
20 historical heavyweight championship fights with birth data.

Fight datetimes are stored in LOCAL time with explicit UTC offset so the
horary chart is cast for the correct UTC moment at the venue.
  e.g. "1986-11-22T22:00:00-08:00" = 10 PM PST at Las Vegas Hilton

Birth datetimes use noon UTC of the known birthdate. No birth time or birth
location is required — only the date matters for natal planet sign positions.

Locations are (latitude, longitude) of the actual fight venue.
"""

FIGHTS = [
    {
        "fight": "Joe Louis vs Jersey Joe Walcott II",
        "datetime": "1948-06-25T22:00:00-04:00",  # 10 PM EDT, Yankee Stadium NY
        "location": (40.8280, -73.9270),  # Yankee Stadium, Bronx NY
        "champion": {
            "name": "Joe Louis",
            "birth_datetime": "1914-05-13T12:00:00Z",  # noon UTC birthdate
            "birth_location": (33.7, -85.0),  # Lafayette, AL (reference only)
        },
        "challenger": {
            "name": "Jersey Joe Walcott",
            "birth_datetime": "1914-01-31T12:00:00Z",
            "birth_location": (39.9, -75.1),  # Merchantville, NJ (reference only)
        },
        "actual_winner": "Joe Louis",
        "method": "KO",
        "round": 11,
    },
    {
        "fight": "Rocky Marciano vs Joe Louis",
        "datetime": "1951-10-26T22:00:00-04:00",  # 10 PM EDT, Madison Square Garden NY
        "location": (40.7505, -73.9934),  # Madison Square Garden (4th), NY
        "champion": {
            "name": "Joe Louis",
            "birth_datetime": "1914-05-13T12:00:00Z",
            "birth_location": (33.7, -85.0),
        },
        "challenger": {
            "name": "Rocky Marciano",
            "birth_datetime": "1923-09-01T12:00:00Z",
            "birth_location": (42.1, -71.0),  # Brockton, MA (reference only)
        },
        "actual_winner": "Rocky Marciano",
        "method": "KO",
        "round": 8,
    },
    {
        "fight": "Rocky Marciano vs Jersey Joe Walcott",
        "datetime": "1952-09-23T22:30:00-04:00",  # 10:30 PM EDT, Philadelphia
        "location": (39.9547, -75.1886),  # Municipal Stadium, Philadelphia PA
        "champion": {
            "name": "Jersey Joe Walcott",
            "birth_datetime": "1914-01-31T12:00:00Z",
            "birth_location": (39.9, -75.1),
        },
        "challenger": {
            "name": "Rocky Marciano",
            "birth_datetime": "1923-09-01T12:00:00Z",
            "birth_location": (42.1, -71.0),
        },
        "actual_winner": "Rocky Marciano",
        "method": "KO",
        "round": 13,
    },
    {
        "fight": "Floyd Patterson vs Archie Moore",
        "datetime": "1956-11-30T22:00:00-06:00",  # 10 PM CST, Chicago Stadium
        "location": (41.8780, -87.6721),  # Chicago Stadium, Chicago IL
        "champion": {
            "name": "Archie Moore",
            "birth_datetime": "1916-12-13T12:00:00Z",
            "birth_location": (33.6, -91.0),  # Benoit, MS (reference only)
        },
        "challenger": {
            "name": "Floyd Patterson",
            "birth_datetime": "1935-01-04T12:00:00Z",
            "birth_location": (35.4, -80.6),  # Waco, NC (reference only)
        },
        "actual_winner": "Floyd Patterson",
        "method": "KO",
        "round": 5,
    },
    {
        "fight": "Floyd Patterson vs Ingemar Johansson",
        "datetime": "1959-06-26T22:00:00-04:00",  # 10 PM EDT, Yankee Stadium NY
        "location": (40.8280, -73.9270),  # Yankee Stadium, Bronx NY
        "champion": {
            "name": "Floyd Patterson",
            "birth_datetime": "1935-01-04T12:00:00Z",
            "birth_location": (35.4, -80.6),
        },
        "challenger": {
            "name": "Ingemar Johansson",
            "birth_datetime": "1932-09-22T12:00:00Z",
            "birth_location": (57.7, 12.0),  # Gothenburg, Sweden (reference only)
        },
        "actual_winner": "Ingemar Johansson",
        "method": "TKO",
        "round": 3,
    },
    {
        "fight": "Floyd Patterson vs Ingemar Johansson II",
        "datetime": "1960-06-20T22:00:00-04:00",  # 10 PM EDT, Polo Grounds NY
        "location": (40.8306, -73.9352),  # Polo Grounds, New York NY
        "champion": {
            "name": "Ingemar Johansson",
            "birth_datetime": "1932-09-22T12:00:00Z",
            "birth_location": (57.7, 12.0),
        },
        "challenger": {
            "name": "Floyd Patterson",
            "birth_datetime": "1935-01-04T12:00:00Z",
            "birth_location": (35.4, -80.6),
        },
        "actual_winner": "Floyd Patterson",
        "method": "KO",
        "round": 5,
    },
    {
        "fight": "Sonny Liston vs Floyd Patterson",
        "datetime": "1962-09-25T21:00:00-05:00",  # 9 PM CDT, Comiskey Park Chicago
        "location": (41.8299, -87.6338),  # Comiskey Park, Chicago IL
        "champion": {
            "name": "Floyd Patterson",
            "birth_datetime": "1935-01-04T12:00:00Z",
            "birth_location": (35.4, -80.6),
        },
        "challenger": {
            "name": "Sonny Liston",
            "birth_datetime": "1932-05-08T12:00:00Z",
            "birth_location": (35.0, -90.8),  # Forrest City, AR (reference only)
        },
        "actual_winner": "Sonny Liston",
        "method": "TKO",
        "round": 1,
    },
    {
        "fight": "Cassius Clay vs Sonny Liston",
        "datetime": "1964-02-25T22:00:00-05:00",  # 10 PM EST, Miami Beach Conv. Hall
        "location": (25.7929, -80.1300),  # Miami Beach Convention Hall, FL
        "champion": {
            "name": "Sonny Liston",
            "birth_datetime": "1932-05-08T12:00:00Z",
            "birth_location": (35.0, -90.8),
        },
        "challenger": {
            "name": "Cassius Clay",
            "birth_datetime": "1942-01-17T12:00:00Z",
            "birth_location": (38.2, -85.7),  # Louisville, KY (reference only)
        },
        "actual_winner": "Cassius Clay",
        "method": "TKO",
        "round": 7,
    },
    {
        "fight": "Muhammad Ali vs Sonny Liston II",
        "datetime": "1965-05-25T22:23:00-04:00",  # 10:23 PM EDT, Lewiston ME
        "location": (44.0994, -70.2148),  # St. Dominic's Arena, Lewiston ME
        "champion": {
            "name": "Muhammad Ali",
            "birth_datetime": "1942-01-17T12:00:00Z",
            "birth_location": (38.2, -85.7),
        },
        "challenger": {
            "name": "Sonny Liston",
            "birth_datetime": "1932-05-08T12:00:00Z",
            "birth_location": (35.0, -90.8),
        },
        "actual_winner": "Muhammad Ali",
        "method": "KO",
        "round": 1,
    },
    {
        "fight": "Muhammad Ali vs Joe Frazier I",
        "datetime": "1971-03-08T22:30:00-05:00",  # 10:30 PM EST, Madison Square Garden NY
        "location": (40.7505, -73.9934),  # Madison Square Garden (4th), NY
        "champion": {
            "name": "Joe Frazier",
            "birth_datetime": "1944-01-12T12:00:00Z",
            "birth_location": (32.4, -80.7),  # Beaufort, SC (reference only)
        },
        "challenger": {
            "name": "Muhammad Ali",
            "birth_datetime": "1942-01-17T12:00:00Z",
            "birth_location": (38.2, -85.7),
        },
        "actual_winner": "Joe Frazier",
        "method": "UD",
        "round": 15,
    },
    {
        "fight": "George Foreman vs Joe Frazier",
        "datetime": "1973-01-22T10:00:00-05:00",  # 10 AM EST (Jamaica), National Arena Kingston
        "location": (17.9990, -76.7937),  # National Arena, Kingston Jamaica
        "champion": {
            "name": "Joe Frazier",
            "birth_datetime": "1944-01-12T12:00:00Z",
            "birth_location": (32.4, -80.7),
        },
        "challenger": {
            "name": "George Foreman",
            "birth_datetime": "1949-01-10T12:00:00Z",
            "birth_location": (32.5, -94.4),  # Marshall, TX (reference only)
        },
        "actual_winner": "George Foreman",
        "method": "TKO",
        "round": 2,
    },
    {
        "fight": "Muhammad Ali vs George Foreman",
        "datetime": "1974-10-30T04:00:00+02:00",  # 4 AM CAT (Kinshasa), Stade du 20 Mai
        "location": (-4.3219, 15.3047),  # Stade du 20 Mai, Kinshasa Zaire
        "champion": {
            "name": "George Foreman",
            "birth_datetime": "1949-01-10T12:00:00Z",
            "birth_location": (32.5, -94.4),
        },
        "challenger": {
            "name": "Muhammad Ali",
            "birth_datetime": "1942-01-17T12:00:00Z",
            "birth_location": (38.2, -85.7),
        },
        "actual_winner": "Muhammad Ali",
        "method": "KO",
        "round": 8,
    },
    {
        "fight": "Muhammad Ali vs Joe Frazier III",
        "datetime": "1975-10-01T10:45:00+08:00",  # 10:45 AM PHT, Araneta Coliseum Manila
        "location": (14.6197, 121.0491),  # Araneta Coliseum, Cubao Manila Philippines
        "champion": {
            "name": "Muhammad Ali",
            "birth_datetime": "1942-01-17T12:00:00Z",
            "birth_location": (38.2, -85.7),
        },
        "challenger": {
            "name": "Joe Frazier",
            "birth_datetime": "1944-01-12T12:00:00Z",
            "birth_location": (32.4, -80.7),
        },
        "actual_winner": "Muhammad Ali",
        "method": "TKO",
        "round": 14,
    },
    {
        "fight": "Muhammad Ali vs Ken Norton III",
        "datetime": "1976-09-28T22:00:00-04:00",  # 10 PM EDT, Yankee Stadium NY
        "location": (40.8280, -73.9270),  # Yankee Stadium, Bronx NY
        "champion": {
            "name": "Muhammad Ali",
            "birth_datetime": "1942-01-17T12:00:00Z",
            "birth_location": (38.2, -85.7),
        },
        "challenger": {
            "name": "Ken Norton",
            "birth_datetime": "1943-08-09T12:00:00Z",
            "birth_location": (39.7, -90.2),  # Jacksonville, IL (reference only)
        },
        "actual_winner": "Muhammad Ali",
        "method": "UD",
        "round": 15,
    },
    {
        "fight": "Larry Holmes vs Ken Norton",
        "datetime": "1978-06-09T22:00:00-07:00",  # 10 PM PDT, Caesars Palace Las Vegas
        "location": (36.1163, -115.1745),  # Caesars Palace, Las Vegas NV
        "champion": {
            "name": "Ken Norton",
            "birth_datetime": "1943-08-09T12:00:00Z",
            "birth_location": (39.7, -90.2),
        },
        "challenger": {
            "name": "Larry Holmes",
            "birth_datetime": "1949-11-03T12:00:00Z",
            "birth_location": (31.8, -84.8),  # Cuthbert, GA (reference only)
        },
        "actual_winner": "Larry Holmes",
        "method": "SD",
        "round": 15,
    },
    {
        "fight": "Mike Tyson vs Trevor Berbick",
        "datetime": "1986-11-22T22:00:00-08:00",  # 10 PM PST, Las Vegas Hilton
        "location": (36.1723, -115.1442),  # Las Vegas Hilton (Westgate), Las Vegas NV
        "champion": {
            "name": "Trevor Berbick",
            "birth_datetime": "1954-08-01T12:00:00Z",
            "birth_location": (18.2, -76.5),  # Port Antonio, Jamaica (reference only)
        },
        "challenger": {
            "name": "Mike Tyson",
            "birth_datetime": "1966-06-30T12:00:00Z",
            "birth_location": (40.7, -73.9),  # Brooklyn, NY (reference only)
        },
        "actual_winner": "Mike Tyson",
        "method": "TKO",
        "round": 2,
    },
    {
        "fight": "Mike Tyson vs Michael Spinks",
        "datetime": "1988-06-27T22:00:00-04:00",  # 10 PM EDT, Convention Center Atlantic City
        "location": (39.3597, -74.4290),  # Atlantic City Convention Center, NJ
        "champion": {
            "name": "Mike Tyson",
            "birth_datetime": "1966-06-30T12:00:00Z",
            "birth_location": (40.7, -73.9),
        },
        "challenger": {
            "name": "Michael Spinks",
            "birth_datetime": "1956-07-13T12:00:00Z",
            "birth_location": (38.6, -90.2),  # St. Louis, MO (reference only)
        },
        "actual_winner": "Mike Tyson",
        "method": "KO",
        "round": 1,
    },
    {
        "fight": "Evander Holyfield vs Mike Tyson I",
        "datetime": "1996-11-09T21:00:00-08:00",  # 9 PM PST, MGM Grand Garden Arena
        "location": (36.1023, -115.1688),  # MGM Grand Garden Arena, Las Vegas NV
        "champion": {
            "name": "Mike Tyson",
            "birth_datetime": "1966-06-30T12:00:00Z",
            "birth_location": (40.7, -73.9),
        },
        "challenger": {
            "name": "Evander Holyfield",
            "birth_datetime": "1962-10-19T12:00:00Z",
            "birth_location": (31.0, -87.5),  # Atmore, AL (reference only)
        },
        "actual_winner": "Evander Holyfield",
        "method": "TKO",
        "round": 11,
    },
    {
        "fight": "Lennox Lewis vs Evander Holyfield II",
        "datetime": "1999-11-13T21:00:00-08:00",  # 9 PM PST, Thomas & Mack Center Las Vegas
        "location": (36.1017, -115.1810),  # Thomas & Mack Center, UNLV Las Vegas NV
        "champion": {
            "name": "Evander Holyfield",
            "birth_datetime": "1962-10-19T12:00:00Z",
            "birth_location": (31.0, -87.5),
        },
        "challenger": {
            "name": "Lennox Lewis",
            "birth_datetime": "1965-09-02T12:00:00Z",
            "birth_location": (51.5, 0.0),  # West Ham, London (reference only)
        },
        "actual_winner": "Lennox Lewis",
        "method": "UD",
        "round": 12,
    },
    {
        "fight": "Lennox Lewis vs Mike Tyson",
        "datetime": "2002-06-08T21:00:00-05:00",  # 9 PM CDT, Pyramid Arena Memphis
        "location": (35.1575, -90.0490),  # Pyramid Arena, Memphis TN
        "champion": {
            "name": "Lennox Lewis",
            "birth_datetime": "1965-09-02T12:00:00Z",
            "birth_location": (51.5, 0.0),
        },
        "challenger": {
            "name": "Mike Tyson",
            "birth_datetime": "1966-06-30T12:00:00Z",
            "birth_location": (40.7, -73.9),
        },
        "actual_winner": "Lennox Lewis",
        "method": "KO",
        "round": 8,
    },
]
