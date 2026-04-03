"""
20 historical heavyweight championship fights with birth data.
All datetimes are UTC (ISO 8601).
Locations are (latitude, longitude).
"""

FIGHTS = [
    {
        "fight": "Joe Louis vs Jersey Joe Walcott II",
        "datetime": "1948-06-25T22:19:00Z",
        "location": (40.7128, -74.0060),  # New York
        "champion": {
            "name": "Joe Louis",
            "birth_datetime": "1914-05-13T19:00:00Z",  # ~14:00 CST
            "birth_location": (33.7, -85.0),  # Lafayette, AL
        },
        "challenger": {
            "name": "Jersey Joe Walcott",
            "birth_datetime": "1914-01-31T15:00:00Z",  # ~10:00 EST
            "birth_location": (39.9, -75.1),  # Merchantville, NJ
        },
        "actual_winner": "Joe Louis",
        "method": "KO",
        "round": 11,
    },
    {
        "fight": "Rocky Marciano vs Joe Louis",
        "datetime": "1951-10-26T02:00:00Z",
        "location": (40.7128, -74.0060),  # New York
        "champion": {
            "name": "Joe Louis",
            "birth_datetime": "1914-05-13T19:00:00Z",
            "birth_location": (33.7, -85.0),
        },
        "challenger": {
            "name": "Rocky Marciano",
            "birth_datetime": "1923-09-01T15:30:00Z",  # ~10:30 EST
            "birth_location": (42.1, -71.0),  # Brockton, MA
        },
        "actual_winner": "Rocky Marciano",
        "method": "KO",
        "round": 8,
    },
    {
        "fight": "Rocky Marciano vs Jersey Joe Walcott",
        "datetime": "1952-09-23T02:30:00Z",
        "location": (39.9, -75.2),  # Philadelphia
        "champion": {
            "name": "Jersey Joe Walcott",
            "birth_datetime": "1914-01-31T15:00:00Z",
            "birth_location": (39.9, -75.1),
        },
        "challenger": {
            "name": "Rocky Marciano",
            "birth_datetime": "1923-09-01T15:30:00Z",
            "birth_location": (42.1, -71.0),
        },
        "actual_winner": "Rocky Marciano",
        "method": "KO",
        "round": 13,
    },
    {
        "fight": "Floyd Patterson vs Archie Moore",
        "datetime": "1956-11-30T03:00:00Z",
        "location": (40.7128, -74.0060),  # New York
        "champion": {
            "name": "Archie Moore",
            "birth_datetime": "1916-12-13T14:00:00Z",  # ~08:00 CST
            "birth_location": (33.6, -91.0),  # Benoit, MS
        },
        "challenger": {
            "name": "Floyd Patterson",
            "birth_datetime": "1935-01-04T14:00:00Z",  # ~09:00 EST
            "birth_location": (35.4, -80.6),  # Waco, NC
        },
        "actual_winner": "Floyd Patterson",
        "method": "KO",
        "round": 5,
    },
    {
        "fight": "Floyd Patterson vs Ingemar Johansson",
        "datetime": "1959-06-26T02:00:00Z",
        "location": (40.7128, -74.0060),  # New York
        "champion": {
            "name": "Floyd Patterson",
            "birth_datetime": "1935-01-04T14:00:00Z",
            "birth_location": (35.4, -80.6),
        },
        "challenger": {
            "name": "Ingemar Johansson",
            "birth_datetime": "1932-09-22T07:00:00Z",  # ~08:00 CET
            "birth_location": (57.7, 12.0),  # Gothenburg, Sweden
        },
        "actual_winner": "Ingemar Johansson",
        "method": "TKO",
        "round": 3,
    },
    {
        "fight": "Floyd Patterson vs Ingemar Johansson II",
        "datetime": "1960-06-20T02:00:00Z",
        "location": (40.7128, -74.0060),  # New York
        "champion": {
            "name": "Ingemar Johansson",
            "birth_datetime": "1932-09-22T07:00:00Z",
            "birth_location": (57.7, 12.0),
        },
        "challenger": {
            "name": "Floyd Patterson",
            "birth_datetime": "1935-01-04T14:00:00Z",
            "birth_location": (35.4, -80.6),
        },
        "actual_winner": "Floyd Patterson",
        "method": "KO",
        "round": 5,
    },
    {
        "fight": "Sonny Liston vs Floyd Patterson",
        "datetime": "1962-09-25T02:00:00Z",
        "location": (41.8781, -87.6298),  # Chicago
        "champion": {
            "name": "Floyd Patterson",
            "birth_datetime": "1935-01-04T14:00:00Z",
            "birth_location": (35.4, -80.6),
        },
        "challenger": {
            "name": "Sonny Liston",
            "birth_datetime": "1932-05-08T15:00:00Z",  # ~09:00 CST
            "birth_location": (35.0, -90.8),  # Forrest City, AR
        },
        "actual_winner": "Sonny Liston",
        "method": "TKO",
        "round": 1,
    },
    {
        "fight": "Cassius Clay vs Sonny Liston",
        "datetime": "1964-02-25T05:00:00Z",
        "location": (25.7617, -80.1918),  # Miami Beach
        "champion": {
            "name": "Sonny Liston",
            "birth_datetime": "1932-05-08T15:00:00Z",
            "birth_location": (35.0, -90.8),
        },
        "challenger": {
            "name": "Cassius Clay",
            "birth_datetime": "1942-01-17T00:35:00Z",  # 18:35 CST on Jan 17 = 00:35 UTC Jan 18
            "birth_location": (38.2, -85.7),  # Louisville, KY
        },
        "actual_winner": "Cassius Clay",
        "method": "TKO",
        "round": 7,
    },
    {
        "fight": "Muhammad Ali vs Sonny Liston II",
        "datetime": "1965-05-25T23:30:00Z",
        "location": (44.3106, -69.7795),  # Lewiston, ME
        "champion": {
            "name": "Muhammad Ali",
            "birth_datetime": "1942-01-17T00:35:00Z",
            "birth_location": (38.2, -85.7),
        },
        "challenger": {
            "name": "Sonny Liston",
            "birth_datetime": "1932-05-08T15:00:00Z",
            "birth_location": (35.0, -90.8),
        },
        "actual_winner": "Muhammad Ali",
        "method": "KO",
        "round": 1,
    },
    {
        "fight": "Muhammad Ali vs Joe Frazier I",
        "datetime": "1971-03-08T23:30:00Z",
        "location": (40.7128, -74.0060),  # New York
        "champion": {
            "name": "Joe Frazier",
            "birth_datetime": "1944-01-12T20:00:00Z",  # ~15:00 EST
            "birth_location": (32.4, -80.7),  # Beaufort, SC
        },
        "challenger": {
            "name": "Muhammad Ali",
            "birth_datetime": "1942-01-17T00:35:00Z",
            "birth_location": (38.2, -85.7),
        },
        "actual_winner": "Joe Frazier",
        "method": "UD",
        "round": 15,
    },
    {
        "fight": "George Foreman vs Joe Frazier",
        "datetime": "1973-01-22T13:00:00Z",
        "location": (-8.9, -36.3),  # Kingston, Jamaica (approx coords: 17.997, -76.793)
        "location": (17.997, -76.793),  # Kingston, Jamaica
        "champion": {
            "name": "Joe Frazier",
            "birth_datetime": "1944-01-12T20:00:00Z",
            "birth_location": (32.4, -80.7),
        },
        "challenger": {
            "name": "George Foreman",
            "birth_datetime": "1949-01-10T16:00:00Z",  # ~10:00 CST
            "birth_location": (32.5, -94.4),  # Marshall, TX
        },
        "actual_winner": "George Foreman",
        "method": "TKO",
        "round": 2,
    },
    {
        "fight": "Muhammad Ali vs George Foreman",
        "datetime": "1974-10-30T02:00:00Z",
        "location": (-4.3, 15.3),  # Kinshasa, Zaire
        "champion": {
            "name": "George Foreman",
            "birth_datetime": "1949-01-10T16:00:00Z",
            "birth_location": (32.5, -94.4),
        },
        "challenger": {
            "name": "Muhammad Ali",
            "birth_datetime": "1942-01-17T00:35:00Z",
            "birth_location": (38.2, -85.7),
        },
        "actual_winner": "Muhammad Ali",
        "method": "KO",
        "round": 8,
    },
    {
        "fight": "Muhammad Ali vs Joe Frazier III",
        "datetime": "1975-10-01T10:45:00Z",
        "location": (14.6, 121.1),  # Manila, Philippines
        "champion": {
            "name": "Muhammad Ali",
            "birth_datetime": "1942-01-17T00:35:00Z",
            "birth_location": (38.2, -85.7),
        },
        "challenger": {
            "name": "Joe Frazier",
            "birth_datetime": "1944-01-12T20:00:00Z",
            "birth_location": (32.4, -80.7),
        },
        "actual_winner": "Muhammad Ali",
        "method": "TKO",
        "round": 14,
    },
    {
        "fight": "Muhammad Ali vs Ken Norton III",
        "datetime": "1976-09-29T02:00:00Z",
        "location": (40.7128, -74.0060),  # New York
        "champion": {
            "name": "Muhammad Ali",
            "birth_datetime": "1942-01-17T00:35:00Z",
            "birth_location": (38.2, -85.7),
        },
        "challenger": {
            "name": "Ken Norton",
            "birth_datetime": "1943-08-09T16:00:00Z",  # ~10:00 CST
            "birth_location": (39.7, -90.2),  # Jacksonville, IL
        },
        "actual_winner": "Muhammad Ali",
        "method": "UD",
        "round": 15,
    },
    {
        "fight": "Larry Holmes vs Ken Norton",
        "datetime": "1978-06-10T04:00:00Z",
        "location": (36.1, -115.2),  # Las Vegas
        "champion": {
            "name": "Ken Norton",
            "birth_datetime": "1943-08-09T16:00:00Z",
            "birth_location": (39.7, -90.2),
        },
        "challenger": {
            "name": "Larry Holmes",
            "birth_datetime": "1949-11-03T14:00:00Z",  # ~09:00 EST
            "birth_location": (31.8, -84.8),  # Cuthbert, GA
        },
        "actual_winner": "Larry Holmes",
        "method": "SD",
        "round": 15,
    },
    {
        "fight": "Mike Tyson vs Trevor Berbick",
        "datetime": "1986-11-22T03:00:00Z",
        "location": (36.1, -115.2),  # Las Vegas
        "champion": {
            "name": "Trevor Berbick",
            "birth_datetime": "1954-08-01T14:00:00Z",  # ~09:00 EST
            "birth_location": (18.2, -76.5),  # Port Antonio, Jamaica
        },
        "challenger": {
            "name": "Mike Tyson",
            "birth_datetime": "1966-06-30T01:30:00Z",  # ~20:30 EST Jun 29
            "birth_location": (40.7, -73.9),  # Brooklyn, NY
        },
        "actual_winner": "Mike Tyson",
        "method": "TKO",
        "round": 2,
    },
    {
        "fight": "Mike Tyson vs Michael Spinks",
        "datetime": "1988-06-28T01:00:00Z",
        "location": (38.9, -77.0),  # Atlantic City, NJ (approx)
        "location": (39.4, -74.4),  # Atlantic City, NJ
        "champion": {
            "name": "Mike Tyson",
            "birth_datetime": "1966-06-30T01:30:00Z",
            "birth_location": (40.7, -73.9),
        },
        "challenger": {
            "name": "Michael Spinks",
            "birth_datetime": "1956-07-13T17:00:00Z",  # ~12:00 CST
            "birth_location": (38.6, -90.2),  # St. Louis, MO
        },
        "actual_winner": "Mike Tyson",
        "method": "KO",
        "round": 1,
    },
    {
        "fight": "Evander Holyfield vs Mike Tyson I",
        "datetime": "1996-11-10T01:30:00Z",
        "location": (36.1, -115.2),  # Las Vegas
        "champion": {
            "name": "Mike Tyson",
            "birth_datetime": "1966-06-30T01:30:00Z",
            "birth_location": (40.7, -73.9),
        },
        "challenger": {
            "name": "Evander Holyfield",
            "birth_datetime": "1962-10-19T15:00:00Z",  # ~10:00 CST
            "birth_location": (31.0, -87.5),  # Atmore, AL
        },
        "actual_winner": "Evander Holyfield",
        "method": "TKO",
        "round": 11,
    },
    {
        "fight": "Lennox Lewis vs Evander Holyfield II",
        "datetime": "1999-11-13T05:00:00Z",
        "location": (36.1, -115.2),  # Las Vegas
        "champion": {
            "name": "Evander Holyfield",
            "birth_datetime": "1962-10-19T15:00:00Z",
            "birth_location": (31.0, -87.5),
        },
        "challenger": {
            "name": "Lennox Lewis",
            "birth_datetime": "1965-09-02T08:30:00Z",
            "birth_location": (51.5, 0.0),  # West Ham, London
        },
        "actual_winner": "Lennox Lewis",
        "method": "UD",
        "round": 12,
    },
    {
        "fight": "Lennox Lewis vs Mike Tyson",
        "datetime": "2002-06-08T23:00:00Z",
        "location": (35.1, -90.0),  # Memphis, TN
        "champion": {
            "name": "Lennox Lewis",
            "birth_datetime": "1965-09-02T08:30:00Z",
            "birth_location": (51.5, 0.0),
        },
        "challenger": {
            "name": "Mike Tyson",
            "birth_datetime": "1966-06-30T01:30:00Z",
            "birth_location": (40.7, -73.9),
        },
        "actual_winner": "Lennox Lewis",
        "method": "KO",
        "round": 8,
    },
]
