"""
database/seed_data.py
─────────────────────
100 real Indian railway stations with accurate metadata.
Fields: code, name, city, state, zone, latitude, longitude, is_major
"""

STATIONS_DATA = [
    # ── Delhi / NCR ─────────────────────────────────────────────────────────
    {"code": "NDLS", "name": "New Delhi",                          "city": "New Delhi",        "state": "Delhi",               "zone": "NR",   "latitude": 28.6448, "longitude": 77.2167, "is_major": True},
    {"code": "NZM",  "name": "Hazrat Nizamuddin",                  "city": "New Delhi",        "state": "Delhi",               "zone": "NR",   "latitude": 28.5823, "longitude": 77.2537, "is_major": True},
    {"code": "DLI",  "name": "Delhi Junction",                     "city": "Delhi",            "state": "Delhi",               "zone": "NR",   "latitude": 28.6563, "longitude": 77.2100, "is_major": False},

    # ── Haryana ─────────────────────────────────────────────────────────────
    {"code": "UMB",  "name": "Ambala Cantt",                       "city": "Ambala",           "state": "Haryana",             "zone": "NR",   "latitude": 30.3782, "longitude": 76.8270, "is_major": False},
    {"code": "ROK",  "name": "Rohtak Junction",                    "city": "Rohtak",           "state": "Haryana",             "zone": "NR",   "latitude": 28.9001, "longitude": 76.5780, "is_major": False},
    {"code": "RE",   "name": "Rewari Junction",                    "city": "Rewari",           "state": "Haryana",             "zone": "NR",   "latitude": 28.1980, "longitude": 76.6175, "is_major": False},

    # ── Punjab ──────────────────────────────────────────────────────────────
    {"code": "ASR",  "name": "Amritsar Junction",                  "city": "Amritsar",         "state": "Punjab",              "zone": "NR",   "latitude": 31.6340, "longitude": 74.8723, "is_major": True},
    {"code": "LDH",  "name": "Ludhiana Junction",                  "city": "Ludhiana",         "state": "Punjab",              "zone": "NR",   "latitude": 30.9010, "longitude": 75.8573, "is_major": True},
    {"code": "CDG",  "name": "Chandigarh",                         "city": "Chandigarh",       "state": "Chandigarh",          "zone": "NR",   "latitude": 30.7333, "longitude": 76.7794, "is_major": True},

    # ── J&K ─────────────────────────────────────────────────────────────────
    {"code": "JAT",  "name": "Jammu Tawi",                         "city": "Jammu",            "state": "Jammu & Kashmir",     "zone": "NR",   "latitude": 32.7266, "longitude": 74.8570, "is_major": True},

    # ── Uttar Pradesh ────────────────────────────────────────────────────────
    {"code": "LKO",  "name": "Lucknow Charbagh",                   "city": "Lucknow",          "state": "Uttar Pradesh",       "zone": "NR",   "latitude": 26.8467, "longitude": 80.9462, "is_major": True},
    {"code": "CNB",  "name": "Kanpur Central",                     "city": "Kanpur",           "state": "Uttar Pradesh",       "zone": "NCR",  "latitude": 26.4499, "longitude": 80.3319, "is_major": True},
    {"code": "AGC",  "name": "Agra Cantt",                         "city": "Agra",             "state": "Uttar Pradesh",       "zone": "NCR",  "latitude": 27.1767, "longitude": 78.0081, "is_major": True},
    {"code": "ALD",  "name": "Prayagraj Junction",                 "city": "Prayagraj",        "state": "Uttar Pradesh",       "zone": "NCR",  "latitude": 25.4358, "longitude": 81.8463, "is_major": True},
    {"code": "BSB",  "name": "Varanasi Junction",                  "city": "Varanasi",         "state": "Uttar Pradesh",       "zone": "NER",  "latitude": 25.3176, "longitude": 82.9739, "is_major": True},
    {"code": "GKP",  "name": "Gorakhpur Junction",                 "city": "Gorakhpur",        "state": "Uttar Pradesh",       "zone": "NER",  "latitude": 26.7551, "longitude": 83.3705, "is_major": True},
    {"code": "MBE",  "name": "Moradabad Junction",                 "city": "Moradabad",        "state": "Uttar Pradesh",       "zone": "NR",   "latitude": 28.8386, "longitude": 78.7733, "is_major": False},
    {"code": "BE",   "name": "Bareilly Junction",                  "city": "Bareilly",         "state": "Uttar Pradesh",       "zone": "NR",   "latitude": 28.3670, "longitude": 79.4304, "is_major": False},
    {"code": "SHC",  "name": "Saharanpur",                         "city": "Saharanpur",       "state": "Uttar Pradesh",       "zone": "NR",   "latitude": 29.9640, "longitude": 77.5460, "is_major": False},

    # ── Uttarakhand ──────────────────────────────────────────────────────────
    {"code": "DDN",  "name": "Dehradun",                           "city": "Dehradun",         "state": "Uttarakhand",         "zone": "NR",   "latitude": 30.3165, "longitude": 78.0322, "is_major": True},
    {"code": "HW",   "name": "Haridwar Junction",                  "city": "Haridwar",         "state": "Uttarakhand",         "zone": "NR",   "latitude": 29.9457, "longitude": 78.1642, "is_major": False},
    {"code": "KGM",  "name": "Kathgodam",                          "city": "Kathgodam",        "state": "Uttarakhand",         "zone": "NR",   "latitude": 29.2168, "longitude": 79.5228, "is_major": False},

    # ── Rajasthan ────────────────────────────────────────────────────────────
    {"code": "JP",   "name": "Jaipur Junction",                    "city": "Jaipur",           "state": "Rajasthan",           "zone": "NWR",  "latitude": 26.9124, "longitude": 75.7873, "is_major": True},
    {"code": "JU",   "name": "Jodhpur Junction",                   "city": "Jodhpur",          "state": "Rajasthan",           "zone": "NWR",  "latitude": 26.2757, "longitude": 73.0243, "is_major": True},
    {"code": "UDZ",  "name": "Udaipur City",                       "city": "Udaipur",          "state": "Rajasthan",           "zone": "NWR",  "latitude": 24.5854, "longitude": 73.7125, "is_major": False},
    {"code": "AJM",  "name": "Ajmer Junction",                     "city": "Ajmer",            "state": "Rajasthan",           "zone": "NWR",  "latitude": 26.4499, "longitude": 74.6399, "is_major": False},
    {"code": "BKN",  "name": "Bikaner Junction",                   "city": "Bikaner",          "state": "Rajasthan",           "zone": "NWR",  "latitude": 28.0229, "longitude": 73.3119, "is_major": False},
    {"code": "KOTA", "name": "Kota Junction",                      "city": "Kota",             "state": "Rajasthan",           "zone": "WCR",  "latitude": 25.2138, "longitude": 75.8648, "is_major": True},

    # ── Madhya Pradesh ───────────────────────────────────────────────────────
    {"code": "BPL",  "name": "Bhopal Junction",                    "city": "Bhopal",           "state": "Madhya Pradesh",      "zone": "WCR",  "latitude": 23.2599, "longitude": 77.4126, "is_major": True},
    {"code": "INDB", "name": "Indore Junction BG",                 "city": "Indore",           "state": "Madhya Pradesh",      "zone": "WR",   "latitude": 22.7196, "longitude": 75.8577, "is_major": True},
    {"code": "RTM",  "name": "Ratlam Junction",                    "city": "Ratlam",           "state": "Madhya Pradesh",      "zone": "WR",   "latitude": 23.3315, "longitude": 75.0367, "is_major": False},

    # ── Gujarat ──────────────────────────────────────────────────────────────
    {"code": "ADI",  "name": "Ahmedabad Junction",                 "city": "Ahmedabad",        "state": "Gujarat",             "zone": "WR",   "latitude": 23.0225, "longitude": 72.5714, "is_major": True},
    {"code": "BRC",  "name": "Vadodara Junction",                  "city": "Vadodara",         "state": "Gujarat",             "zone": "WR",   "latitude": 22.3144, "longitude": 73.1812, "is_major": True},
    {"code": "ST",   "name": "Surat",                              "city": "Surat",            "state": "Gujarat",             "zone": "WR",   "latitude": 21.2060, "longitude": 72.8370, "is_major": False},
    {"code": "RJT",  "name": "Rajkot Junction",                    "city": "Rajkot",           "state": "Gujarat",             "zone": "WR",   "latitude": 22.3039, "longitude": 70.8022, "is_major": False},
    {"code": "ANND", "name": "Anand Junction",                     "city": "Anand",            "state": "Gujarat",             "zone": "WR",   "latitude": 22.5584, "longitude": 72.9284, "is_major": False},
    {"code": "GDA",  "name": "Godhra Junction",                    "city": "Godhra",           "state": "Gujarat",             "zone": "WR",   "latitude": 22.7789, "longitude": 73.6143, "is_major": False},
    {"code": "VAPI", "name": "Vapi",                               "city": "Vapi",             "state": "Gujarat",             "zone": "WR",   "latitude": 20.3717, "longitude": 72.9101, "is_major": False},
    {"code": "JND",  "name": "Jamnagar",                           "city": "Jamnagar",         "state": "Gujarat",             "zone": "WR",   "latitude": 22.4707, "longitude": 70.0577, "is_major": False},
    {"code": "PBR",  "name": "Porbandar",                          "city": "Porbandar",        "state": "Gujarat",             "zone": "WR",   "latitude": 21.6425, "longitude": 69.6053, "is_major": False},
    {"code": "OKHA", "name": "Okha",                               "city": "Okha",             "state": "Gujarat",             "zone": "WR",   "latitude": 22.4742, "longitude": 69.0694, "is_major": False},
    {"code": "VRL",  "name": "Veraval",                            "city": "Veraval",          "state": "Gujarat",             "zone": "WR",   "latitude": 20.9070, "longitude": 70.3645, "is_major": False},

    # ── Maharashtra ──────────────────────────────────────────────────────────
    {"code": "CSTM", "name": "Chhatrapati Shivaji Maharaj Terminus","city": "Mumbai",          "state": "Maharashtra",         "zone": "CR",   "latitude": 18.9398, "longitude": 72.8355, "is_major": True},
    {"code": "MMCT", "name": "Mumbai Central",                     "city": "Mumbai",           "state": "Maharashtra",         "zone": "WR",   "latitude": 18.9700, "longitude": 72.8195, "is_major": True},
    {"code": "BDTS", "name": "Bandra Terminus",                    "city": "Mumbai",           "state": "Maharashtra",         "zone": "WR",   "latitude": 19.0541, "longitude": 72.8396, "is_major": False},
    {"code": "LTT",  "name": "Lokmanya Tilak Terminus",            "city": "Mumbai",           "state": "Maharashtra",         "zone": "CR",   "latitude": 19.0687, "longitude": 72.9070, "is_major": False},
    {"code": "DR",   "name": "Dadar",                              "city": "Mumbai",           "state": "Maharashtra",         "zone": "CR",   "latitude": 19.0178, "longitude": 72.8429, "is_major": False},
    {"code": "PUNE", "name": "Pune Junction",                      "city": "Pune",             "state": "Maharashtra",         "zone": "CR",   "latitude": 18.5204, "longitude": 73.8567, "is_major": True},
    {"code": "NGP",  "name": "Nagpur Junction",                    "city": "Nagpur",           "state": "Maharashtra",         "zone": "SECR", "latitude": 21.1458, "longitude": 79.0882, "is_major": True},
    {"code": "SUR",  "name": "Solapur Junction",                   "city": "Solapur",          "state": "Maharashtra",         "zone": "CR",   "latitude": 17.6805, "longitude": 75.9064, "is_major": False},
    {"code": "AKL",  "name": "Akola Junction",                     "city": "Akola",            "state": "Maharashtra",         "zone": "CR",   "latitude": 20.7002, "longitude": 77.0082, "is_major": False},
    {"code": "NED",  "name": "Nanded Junction",                    "city": "Nanded",           "state": "Maharashtra",         "zone": "SCR",  "latitude": 19.1383, "longitude": 77.3210, "is_major": False},

    # ── Goa ─────────────────────────────────────────────────────────────────
    {"code": "MAO",  "name": "Madgaon Junction",                   "city": "Margao",           "state": "Goa",                 "zone": "KR",   "latitude": 15.3567, "longitude": 73.9580, "is_major": False},

    # ── Karnataka ────────────────────────────────────────────────────────────
    {"code": "SBC",  "name": "KSR Bengaluru City",                 "city": "Bengaluru",        "state": "Karnataka",           "zone": "SWR",  "latitude": 12.9716, "longitude": 77.5946, "is_major": True},
    {"code": "MYS",  "name": "Mysuru Junction",                    "city": "Mysuru",           "state": "Karnataka",           "zone": "SWR",  "latitude": 12.3052, "longitude": 76.6551, "is_major": True},
    {"code": "UBL",  "name": "Hubballi Junction",                  "city": "Hubballi",         "state": "Karnataka",           "zone": "SWR",  "latitude": 15.3647, "longitude": 75.1240, "is_major": False},
    {"code": "MAJN", "name": "Mangaluru Junction",                 "city": "Mangaluru",        "state": "Karnataka",           "zone": "SWR",  "latitude": 12.9165, "longitude": 74.8560, "is_major": False},

    # ── Tamil Nadu ───────────────────────────────────────────────────────────
    {"code": "MAS",  "name": "Chennai Central",                    "city": "Chennai",          "state": "Tamil Nadu",          "zone": "SR",   "latitude": 13.0827, "longitude": 80.2707, "is_major": True},
    {"code": "CBE",  "name": "Coimbatore Junction",                "city": "Coimbatore",       "state": "Tamil Nadu",          "zone": "SR",   "latitude": 11.0018, "longitude": 76.9628, "is_major": True},
    {"code": "MDU",  "name": "Madurai Junction",                   "city": "Madurai",          "state": "Tamil Nadu",          "zone": "SR",   "latitude":  9.9252, "longitude": 78.1198, "is_major": True},
    {"code": "TPJ",  "name": "Tiruchirappalli Junction",           "city": "Tiruchirappalli",  "state": "Tamil Nadu",          "zone": "SR",   "latitude": 10.8505, "longitude": 78.6847, "is_major": False},
    {"code": "SA",   "name": "Salem Junction",                     "city": "Salem",            "state": "Tamil Nadu",          "zone": "SR",   "latitude": 11.6643, "longitude": 78.1460, "is_major": False},
    {"code": "TEN",  "name": "Tirunelveli Junction",               "city": "Tirunelveli",      "state": "Tamil Nadu",          "zone": "SR",   "latitude":  8.7139, "longitude": 77.7567, "is_major": False},

    # ── Kerala ───────────────────────────────────────────────────────────────
    {"code": "TVC",  "name": "Thiruvananthapuram Central",         "city": "Thiruvananthapuram","state": "Kerala",             "zone": "SR",   "latitude":  8.4855, "longitude": 76.9492, "is_major": True},
    {"code": "ERS",  "name": "Ernakulam Junction",                 "city": "Kochi",            "state": "Kerala",             "zone": "SR",   "latitude":  9.9816, "longitude": 76.2999, "is_major": True},
    {"code": "PGT",  "name": "Palakkad Junction",                  "city": "Palakkad",         "state": "Kerala",             "zone": "SR",   "latitude": 10.7867, "longitude": 76.6548, "is_major": False},

    # ── Andhra Pradesh ───────────────────────────────────────────────────────
    {"code": "BZA",  "name": "Vijayawada Junction",                "city": "Vijayawada",       "state": "Andhra Pradesh",      "zone": "SCR",  "latitude": 16.5062, "longitude": 80.6480, "is_major": True},
    {"code": "VSKP", "name": "Visakhapatnam Junction",             "city": "Visakhapatnam",    "state": "Andhra Pradesh",      "zone": "ECoR", "latitude": 17.6868, "longitude": 83.2185, "is_major": True},
    {"code": "GNT",  "name": "Guntur Junction",                    "city": "Guntur",           "state": "Andhra Pradesh",      "zone": "SCR",  "latitude": 16.3067, "longitude": 80.4365, "is_major": False},
    {"code": "RJY",  "name": "Rajahmundry",                        "city": "Rajahmundry",      "state": "Andhra Pradesh",      "zone": "SCR",  "latitude": 17.0005, "longitude": 81.7799, "is_major": False},
    {"code": "TPTY", "name": "Tirupati",                           "city": "Tirupati",         "state": "Andhra Pradesh",      "zone": "SCR",  "latitude": 13.6288, "longitude": 79.4192, "is_major": True},

    # ── Telangana ────────────────────────────────────────────────────────────
    {"code": "SC",   "name": "Secunderabad Junction",              "city": "Hyderabad",        "state": "Telangana",           "zone": "SCR",  "latitude": 17.4399, "longitude": 78.4983, "is_major": True},
    {"code": "HYB",  "name": "Hyderabad Deccan",                   "city": "Hyderabad",        "state": "Telangana",           "zone": "SCR",  "latitude": 17.3850, "longitude": 78.4867, "is_major": False},

    # ── Odisha ───────────────────────────────────────────────────────────────
    {"code": "BBS",  "name": "Bhubaneswar",                        "city": "Bhubaneswar",      "state": "Odisha",              "zone": "ECoR", "latitude": 20.2961, "longitude": 85.8245, "is_major": True},
    {"code": "PURI", "name": "Puri",                               "city": "Puri",             "state": "Odisha",              "zone": "ECoR", "latitude": 19.8006, "longitude": 85.8149, "is_major": False},
    {"code": "CTC",  "name": "Cuttack Junction",                   "city": "Cuttack",          "state": "Odisha",              "zone": "ECoR", "latitude": 20.4625, "longitude": 85.8830, "is_major": False},
    {"code": "SBP",  "name": "Sambalpur Road",                     "city": "Sambalpur",        "state": "Odisha",              "zone": "ECoR", "latitude": 21.4669, "longitude": 83.9756, "is_major": False},
    {"code": "RU",   "name": "Rourkela Junction",                  "city": "Rourkela",         "state": "Odisha",              "zone": "SER",  "latitude": 22.2604, "longitude": 84.8536, "is_major": False},

    # ── West Bengal ──────────────────────────────────────────────────────────
    {"code": "HWH",  "name": "Howrah Junction",                    "city": "Kolkata",          "state": "West Bengal",         "zone": "ER",   "latitude": 22.5839, "longitude": 88.3424, "is_major": True},
    {"code": "SDAH", "name": "Sealdah",                            "city": "Kolkata",          "state": "West Bengal",         "zone": "ER",   "latitude": 22.5651, "longitude": 88.3700, "is_major": True},
    {"code": "KOAA", "name": "Kolkata Chitpur",                    "city": "Kolkata",          "state": "West Bengal",         "zone": "ER",   "latitude": 22.5958, "longitude": 88.3697, "is_major": False},
    {"code": "NJP",  "name": "New Jalpaiguri",                     "city": "Siliguri",         "state": "West Bengal",         "zone": "NFR",  "latitude": 26.7069, "longitude": 88.2647, "is_major": True},
    {"code": "ASN",  "name": "Asansol Junction",                   "city": "Asansol",          "state": "West Bengal",         "zone": "ER",   "latitude": 23.6906, "longitude": 86.9606, "is_major": False},
    {"code": "BWN",  "name": "Barddhaman Junction",                "city": "Barddhaman",       "state": "West Bengal",         "zone": "ER",   "latitude": 23.2324, "longitude": 87.8615, "is_major": False},
    {"code": "MLDT", "name": "Malda Town",                         "city": "Malda",            "state": "West Bengal",         "zone": "ER",   "latitude": 25.0108, "longitude": 88.1418, "is_major": False},
    {"code": "KGP",  "name": "Kharagpur Junction",                 "city": "Kharagpur",        "state": "West Bengal",         "zone": "SER",  "latitude": 22.3460, "longitude": 87.3119, "is_major": False},
    {"code": "PTRU", "name": "Purulia Junction",                   "city": "Purulia",          "state": "West Bengal",         "zone": "SER",  "latitude": 23.3300, "longitude": 86.3600, "is_major": False},

    # ── Bihar ────────────────────────────────────────────────────────────────
    {"code": "PNBE", "name": "Patna Junction",                     "city": "Patna",            "state": "Bihar",               "zone": "ECR",  "latitude": 25.6093, "longitude": 85.1235, "is_major": True},
    {"code": "MFP",  "name": "Muzaffarpur Junction",               "city": "Muzaffarpur",      "state": "Bihar",               "zone": "ECR",  "latitude": 26.1209, "longitude": 85.3647, "is_major": False},
    {"code": "GAYA", "name": "Gaya Junction",                      "city": "Gaya",             "state": "Bihar",               "zone": "ECR",  "latitude": 24.7955, "longitude": 85.0002, "is_major": False},

    # ── Jharkhand ────────────────────────────────────────────────────────────
    {"code": "DHN",  "name": "Dhanbad Junction",                   "city": "Dhanbad",          "state": "Jharkhand",           "zone": "ECR",  "latitude": 23.7957, "longitude": 86.4304, "is_major": False},
    {"code": "RNC",  "name": "Ranchi Junction",                    "city": "Ranchi",           "state": "Jharkhand",           "zone": "SER",  "latitude": 23.3441, "longitude": 85.3096, "is_major": True},
    {"code": "TAT",  "name": "Tatanagar Junction",                 "city": "Jamshedpur",       "state": "Jharkhand",           "zone": "SER",  "latitude": 22.7924, "longitude": 86.1858, "is_major": False},
    {"code": "HTE",  "name": "Hatia",                              "city": "Ranchi",           "state": "Jharkhand",           "zone": "SER",  "latitude": 23.3234, "longitude": 85.2700, "is_major": False},
    {"code": "JSME", "name": "Jasidih Junction",                   "city": "Jasidih",          "state": "Jharkhand",           "zone": "ER",   "latitude": 24.5168, "longitude": 86.6455, "is_major": False},

    # ── Assam ────────────────────────────────────────────────────────────────
    {"code": "GHY",  "name": "Guwahati",                           "city": "Guwahati",         "state": "Assam",               "zone": "NFR",  "latitude": 26.1445, "longitude": 91.7362, "is_major": True},
    {"code": "DBRT", "name": "Dibrugarh Town",                     "city": "Dibrugarh",        "state": "Assam",               "zone": "NFR",  "latitude": 27.4728, "longitude": 94.9120, "is_major": False},

    # ── Tripura / Northeast ──────────────────────────────────────────────────
    {"code": "AGTL", "name": "Agartala",                           "city": "Agartala",         "state": "Tripura",             "zone": "NFR",  "latitude": 23.8315, "longitude": 91.2868, "is_major": False},

    # ── Chhattisgarh ─────────────────────────────────────────────────────────
    {"code": "R",    "name": "Raipur Junction",                    "city": "Raipur",           "state": "Chhattisgarh",        "zone": "SECR", "latitude": 21.2340, "longitude": 81.6340, "is_major": True},

    # ── Himachal Pradesh ─────────────────────────────────────────────────────
    {"code": "UHL",  "name": "Una Himachal",                       "city": "Una",              "state": "Himachal Pradesh",    "zone": "NR",   "latitude": 31.4680, "longitude": 76.2700, "is_major": False},
]
