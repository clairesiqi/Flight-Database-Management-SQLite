

# ---------------------------------UPDATE----------------------------------#
def update():

  # assign new window and dropdown list by calling heading generator

  update_window, table_dropdown = menu_heading(master, "update")

  # create empty containers to store field labels and entry boxes
  label_dict = {}
  entry_dict = {}
  constraints_dict = {}
  fields = []

  def table_viewer():
    # table viewer window
    if table_dropdown.get() == "Please select":
      messagebox.showerror("Error",
                           "Please select a table",
                           parent=update_window)
      return

    table_viewer_window = Toplevel(update_window)
    table_viewer_window.minsize(width=600, height=500)
    table_viewer_window.title(f"{table_dropdown.get()} Records")

    c.execute(f"SELECT * FROM {table_dropdown.get()}")
    records = c.fetchall()
    columns = tuple([description[0] for description in c.description])
    table_view = ttk.Treeview(table_viewer_window,
                              columns=columns,
                              show="headings")

    for i in range(len(columns)):
      table_view.heading(columns[i], text=columns[i])
    table_view.pack()
    for obs in records:
      table_view.update('', 'end', values=obs)
    # get the count of rows retrieved and show in view title
    c.execute(f"SELECT count(*) FROM {table_dropdown.get()}")
    row_count = c.fetchone()[0]
    table_viewer_window.title(
        f"{table_dropdown.get()} Search View: {row_count} observations found")
    return

  # declare function to show fields and textboxes

  def show_fields_textbox(event):

    # Get the selected table name and all field names
    table_name = table_dropdown.get()
    c.execute(f"SELECT * FROM {table_name}")
    fields = [description[0] for description in c.description]
    if table_name == "Pilots":
      fields.append("FlightID")
    if table_name == "Flights":
      fields.append("PilotID")
    # delete existing labels and entryboxes
    for label in label_dict.values():
      label.destroy()
    for entry in entry_dict.values():
      entry.destroy()
    for constraint in constraints_dict.values():
      constraint.destroy()
    # create new labels and entryboxes
    # set axis
    x = 20
    y = 70

    c.execute("SELECT FlightID FROM Flights")
    flightIDs = c.fetchall()
    flightID_existing = [flight[0] for flight in flightIDs]

    c.execute("SELECT PilotID FROM Pilots")
    pilotIDs = c.fetchall()
    pilotID_existing = [pilot[0] for pilot in pilotIDs]

    for field in fields:
      # create label
      label_dict[field] = Label(update_window, text=field)

      # create input box and add constraints
      ## -------------------------------------------------------Pilot table
      if table_name == "Pilots":
        ### create dropdown boxes for restricted fields
        # ALL flightIDs

        if field == "Gender":
          entry_dict[field] = ttk.Combobox(update_window,
                                           state="readonly",
                                           values=gender_list)
        elif field == "Nationality":
          entry_dict[field] = ttk.Combobox(update_window,
                                           state="readonly",
                                           values=nationalities)
        elif field == "Seniority":
          entry_dict[field] = ttk.Combobox(update_window,
                                           state="readonly",
                                           values=seniorities)
        elif field == "FlightID":
          entry_dict[field] = Listbox(update_window, selectmode="multiple")

          for flightID in flightID_existing:
            entry_dict[field].update(flightID_existing.index(flightID),
                                     flightID)
        else:
          entry_dict[field] = Entry(update_window)

        # place label and input box
        label_dict[field].place(x=x, y=y)
        entry_dict[field].place(x=x + 130, y=y)
        if field == "PilotID":
          constraints_dict[field] = Label(update_window,
                                          text="6-digit code, e.g. AA03XY",
                                          font=(font, 8, 'italic'),
                                          fg="gray")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "FirstName":
          constraints_dict[field] = Label(update_window,
                                          text="e.g. William",
                                          font=(font, 8, 'italic'),
                                          fg="gray")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "LastName":
          constraints_dict[field] = Label(update_window,
                                          text="e.g. Smith",
                                          font=(font, 8, 'italic'),
                                          fg="gray")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "MiddleName":
          constraints_dict[field] = Label(update_window,
                                          text="(Optional)",
                                          font=(font, 8, 'italic'),
                                          fg="gray")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "DateOfBirth" or field == "DateHired":
          constraints_dict[field] = Label(update_window,
                                          text="YYYY-MM-DD, e.g. 1999-12-31",
                                          font=(
                                              font,
                                              8,
                                              'italic',
                                          ),
                                          fg="gray")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "LicenseNumber":
          constraints_dict[field] = Label(
              update_window,
              text="11-digit code, e.g. QWER1234UIO",
              font=(font, 8, 'italic'),
              fg="gray")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "FlightHours":
          constraints_dict[field] = Label(update_window,
                                          text="Total hours flying, e.g. 120",
                                          font=(font, 8, 'italic'),
                                          fg="gray")
          constraints_dict[field].place(x=x + 310, y=y)

        if field == "Email":
          constraints_dict[field] = Label(
              update_window,
              text="Required: Contact email address, e.g. JohnDoe@gmail.com",
              font=(font, 8, 'italic'),
              fg="gray")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "FlightID":
          constraints_dict[field] = Label(
              update_window,
              text="Select all Flights (IDs) this pilot operates",
              font=(font, 8, 'italic'),
              fg="gray")
          constraints_dict[field].place(x=x + 310, y=y)

        # increment y axis
        y += 30

      ## -------------------------------------------------------- Flight table
      if table_name == "Flights":
        aircraft_ids = c.execute('''select AircraftID from Aircrafts''')
        aircraft_ids = [aircraft_id[0] for aircraft_id in aircraft_ids]
        if field == "Type":
          entry_dict[field] = ttk.Combobox(update_window,
                                           state="readonly",
                                           values=flight_type_list)
        elif field == "AircraftID":
          entry_dict[field] = ttk.Combobox(update_window,
                                           state="readonly",
                                           values=aircraft_ids)
        # listbox for foreign key
        elif field == "PilotID":
          entry_dict[field] = Listbox(update_window, selectmode="multiple")

          for pilotID in pilotID_existing:
            entry_dict[field].update(pilotID_existing.index(pilotID), pilotID)

        else:
          entry_dict[field] = Entry(update_window)

        # place label and input box
        label_dict[field].place(x=x, y=y)
        entry_dict[field].place(x=x + 130, y=y)

        # add constraint notes
        if field == "FlightID":
          constraints_dict[field] = Label(update_window,
                                          text="5-10-digit code, e.g. BA777",
                                          font=(font, 8, 'italic'),
                                          fg="gray")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "DepartureAirport":
          constraints_dict[field] = Label(
              update_window,
              text="3-letter airport code, e.g. JFK",
              font=(font, 8, 'italic'),
              fg="gray")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "ArrivalAirport":
          constraints_dict[field] = Label(
              update_window,
              text="3-letter airport code, e.g. JFKh",
              font=(font, 8, 'italic'),
              fg="gray")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "AircraftID":
          constraints_dict[field] = Label(
              update_window,
              text=
              "Select from saved IDs, update into Aircrafts table if new aircraft",
              font=(font, 8, 'italic'),
              fg="gray")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "FlightDuration":
          constraints_dict[field] = Label(
              update_window,
              text="Enter in format 'XhXmin' e.g. 3h22min",
              font=(font, 8, 'italic'),
              fg="gray")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "DepartureDate":
          constraints_dict[field] = Label(update_window,
                                          text="YYYY-MM-DD, e.g. 2023-12-31",
                                          font=(
                                              font,
                                              8,
                                              'italic',
                                          ),
                                          fg="gray")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "DepartureTime":
          constraints_dict[field] = Label(update_window,
                                          text="HH:MM, e.g. 08:04, 14:55",
                                          font=(
                                              font,
                                              8,
                                              'italic',
                                          ),
                                          fg="gray")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "PilotID":
          constraints_dict[field] = Label(
              update_window,
              text="Select all pilots (IDs) this flight is assigned to.",
              font=(font, 8, 'italic'),
              fg="gray")
          constraints_dict[field].place(x=x + 310, y=y)
        # increment y axis
        y += 30

      ## -------------------------------------------------------- Aircraft table

      if table_name == "Aircrafts":
        ### create dropdown boxes for restricted fields
        if field == "Model":
          entry_dict[field] = ttk.Combobox(update_window,
                                           state="readonly",
                                           values=models_list)
        elif field == "Manufacturer":
          entry_dict[field] = ttk.Combobox(update_window,
                                           state="readonly",
                                           values=manufacturer_list)
        elif field == "EngineType":
          entry_dict[field] = ttk.Combobox(update_window,
                                           state="readonly",
                                           values=aircraft_engine_types)
        elif field == "OwnershipType":
          entry_dict[field] = ttk.Combobox(update_window,
                                           state="readonly",
                                           values=aircraft_ownership_types)
        elif field == "Insured":
          entry_dict[field] = ttk.Combobox(update_window,
                                           state="readonly",
                                           values=insured)
        else:
          entry_dict[field] = Entry(update_window)

        # place label and input box
        label_dict[field].place(x=x, y=y)
        entry_dict[field].place(x=x + 130, y=y)
        if field == "AircraftID":
          constraints_dict[field] = Label(
              update_window,
              text="10-digit code, e.g. AA03XYZ678",
              font=(font, 8, 'italic'),
              fg="gray")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "RegistrationNumber":
          constraints_dict[field] = Label(update_window,
                                          text="8-digit code, e.g. 03XYZ678",
                                          font=(font, 8, 'italic'),
                                          fg="gray")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "ManufacturingDate":
          constraints_dict[field] = Label(update_window,
                                          text="YYYY-MM-DD, e.g. 2019-12-31",
                                          font=(font, 8, 'italic'),
                                          fg="gray")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "SeatingCapacity":
          constraints_dict[field] = Label(update_window,
                                          text="Positive Integer, e.g. 250",
                                          font=(font, 8, 'italic'),
                                          fg="gray")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "FuelCapacity":
          constraints_dict[field] = Label(
              update_window,
              text="Positive Integer (in gallons), e.g. 78747",
              font=(font, 8, 'italic'),
              fg="gray")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "MaximumDistance":
          constraints_dict[field] = Label(
              update_window,
              text="In miles, maximum 2 decimals, e.g. 1240.88",
              font=(
                  font,
                  8,
                  'italic',
              ),
              fg="gray")
          constraints_dict[field].place(x=x + 310, y=y)

        # increment y axis
        y += 30

      ## -------------------------------------------------------- Destination table
      if table_name == "Destinations":
        ### create dropdown boxes for restricted fields
        if field == "Country":
          entry_dict[field] = ttk.Combobox(update_window,
                                           state="readonly",
                                           values=country_list)
        elif field == "Timezone":
          entry_dict[field] = ttk.Combobox(update_window,
                                           state="readonly",
                                           values=timezones)
        else:
          entry_dict[field] = Entry(update_window)

        def on_trigger(event):
          entry_dict["DestinationAirport"].delete(0, END)
          ID_value = entry_dict["DestinationID"].get().strip().upper()
          if ID_value in airport_info:
            entry_dict["DestinationAirport"].update(
                END, string=airport_info[ID_value])
          return

        entry_dict["DestinationID"].bind("<KeyRelease>", on_trigger)
        # place label and input box
        label_dict[field].place(x=x, y=y)
        entry_dict[field].place(x=x + 130, y=y)

        # add constraint notes
        if field == "DestinationID":
          constraints_dict[field] = Label(
              update_window,
              text="3-letter airport code, e.g. JFK",
              font=(font, 8, 'italic'),
              fg="gray")
          constraints_dict[field].place(x=x + 310, y=y)
        if field == "City":
          constraints_dict[field] = Label(update_window,
                                          text="City name, e.g. New York",
                                          font=(font, 8, 'italic'),
                                          fg="gray")
          constraints_dict[field].place(x=x + 310, y=y)

        # increment y axis
        y += 30

    return








  

  # check [INPUT VALIDITY] for all fields
  def update_confirm():

    # -----------------PILOTS-------------------#
    if table_dropdown.get() == "Pilots":

      # list of all error messages to display
      error_list = []

      # Unique Primary Key
      c.execute('''select PilotID from Pilots''')
      pilotIDs = c.fetchall()
      key_values = [pilotID[0] for pilotID in pilotIDs]
      if entry_dict["PilotID"].get() in key_values:
        error_list.append(
            f"{len(error_list)+1}. PilotID already exist in record. Primary key cannot have duplicate values."
        )

      if entry_dict["PilotID"].get() == "":
        error_list.append(f"{len(error_list)+1}. PilotID cannot be empty.")

      if not re.match(r'^[a-zA-Z0-9]{6}$', entry_dict['PilotID'].get()):
        error_list.append(
            f"{len(error_list)+1}. PilotID must be 6-digit code consisting of only letters A-Z and numbers 0-9."
        )
      # DateOfBirth, DateHired must be dd/mm/yyyy
      if entry_dict["DateOfBirth"].get() != "" and not re.match(
          r'\d{4}-\d{2}-\d{2}$', entry_dict["DateOfBirth"].get()):
        error_list.append(
            f"{len(error_list)+1}. DateOfBirth must be YYYY-MM-DD format.")

      if entry_dict["DateHired"].get() != "" and not re.match(
          r'\d{4}-\d{2}-\d{2}', entry_dict["DateHired"].get()):
        error_list.append(
            f"{len(error_list)+1}. DateHired must be YYYY-MM-DD format.")

      # Name must be String of text (letters in the alphabet)
      if entry_dict["FirstName"].get() != "" and not re.match(
          r'^[a-zA-Z]+$', entry_dict["FirstName"].get()):
        error_list.append(
            f"{len(error_list)+1}. FirstName must be a String of text (letters in the alphabet)."
        )

      if entry_dict["LastName"].get() != "" and not re.match(
          r'^[a-zA-Z]+$', entry_dict["LastName"].get()):
        error_list.append(
            f"{len(error_list)+1}. LastName must be a String of text (letters in the alphabet)."
        )

      if entry_dict["MiddleName"].get() != "" and not re.match(
          r'^[a-zA-Z]+$', entry_dict["LastName"].get()):
        error_list.append(
            f"{len(error_list)+1}. MiddleName must be a String of text (letters in the alphabet)."
        )

      # LicenseNumber must be 11 digits of Letters and numbers
      if entry_dict["LicenseNumber"].get() != "" and not re.match(
          r'^[a-zA-Z0-9]{11}$', entry_dict["LicenseNumber"].get()):
        error_list.append(
            f"{len(error_list)+1}. LicenseNumber must be 11-digit code consisting of only letters A-Z and numbers 0-9."
        )

      # FlightHours must be an integer
      if entry_dict['FlightHours'].get() != "" and not re.match(
          r'^[0-9]+$', entry_dict['FlightHours'].get()):
        error_list.append(
            f"{len(error_list)}. FlightHours must be a positive integer.")

      # FlightHours must be an integer
      if not re.match(r'^[\w\.-]+@[\w\.-]+$', entry_dict['Email'].get()):
        error_list.append(f"{len(error_list)}. Invalid email address.")
      # ------All fields check complete--------#
      if len(error_list) > 0:
        error_message = ""
        for error in error_list:
          error_message += error
          error_message += "\n"
        messagebox.showerror(parent=update_window,
                             title="Error",
                             message="Invalid data input",
                             detail=error_message)
      # if all values qualify, update to table.
      else:
        # ask user to double check inputs
        confirm = messagebox.askyesno(
            parent=update_window,
            title="Confirm Submission",
            message="Please check the data input. Is it correct?")
        if confirm:
          # fetch all input values and update into Pilot Table
          pilot_id = entry_dict["PilotID"].get().upper()
          email = entry_dict["Email"].get().lower()
          first_name = entry_dict["FirstName"].get().title()
          middle_name = entry_dict["MiddleName"].get().title()
          last_name = entry_dict["LastName"].get().title()
          gender = entry_dict["Gender"].get()
          nationality = entry_dict["Nationality"].get()
          date_of_birth = entry_dict["DateOfBirth"].get()
          license_number = entry_dict["LicenseNumber"].get()
          date_hired = entry_dict["DateHired"].get()

          flight_hours = entry_dict["FlightHours"].get()
          flight_hours = int(flight_hours) if flight_hours != "" else -1
          seniority = entry_dict["Seniority"].get()

          c.execute(
              '''
              update INTO PILOTS VALUES 
              (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
              ''',
              (pilot_id, email, first_name if first_name != "" else None,
               middle_name if middle_name != "" else None, last_name
               if last_name != "" else None, gender if gender != "" else None,
               nationality if nationality != "" else None,
               None if date_of_birth == "" else date_of_birth,
               license_number if license_number != 0 else None,
               None if date_hired == "" else date_hired,
               flight_hours if flight_hours != -1 else None,
               seniority if seniority != "" else None))
          conn.commit()
          # show messagebox confirming updateion
          messagebox.showinfo(parent=update_window,
                              title="Success",
                              message="Record updateed!")

          # fetch all listbox values and update to pilot-flight Junction table
          associated_flights = [
              entry_dict['FlightID'].get(index)
              for index in entry_dict['FlightID'].curselection()
          ]
          if len(associated_flights) > 0:
            for flight_id in associated_flights:
              c.execute(f'''
              update INTO Pilot_Flight_JUNC VALUES 
              ('{pilot_id}','{flight_id}')
              ''')
              conn.commit()

    # -----------------Destinations-------------------#
    if table_dropdown.get() == "Destinations":

      # list of all error messages to display
      error_list = []

      # Unique Primary Key
      c.execute('''select DestinationID from Destinations''')
      destinationIDs = c.fetchall()
      key_values = [destinationID[0] for destinationID in destinationIDs]
      if entry_dict["DestinationID"].get() in key_values:
        error_list.append(
            f"{len(error_list)+1}. DestinationID already exist in record. Primary key cannot have duplicate values."
        )

      if entry_dict["DestinationID"].get() == "":
        error_list.append(
            f"{len(error_list)+1}. DestinationID cannot be empty.")

      if not re.match(r'[A-Za-z]{3}', entry_dict['DestinationID'].get()):
        error_list.append(
            f"{len(error_list)+1}. DestinationID must be 3-letter airport code."
        )
      # DateOfBirth, DateHired must be yyyy/mm/dd
      if entry_dict["City"].get() != "" and not re.match(
          r'[A-Za-z\s]+', entry_dict["City"].get()):
        error_list.append(f"{len(error_list)+1}. Invalid city name.")

      if entry_dict["DestinationAirport"].get() != "" and not re.match(
          r"[A-Za-z\s']+", entry_dict["DestinationAirport"].get()):
        error_list.append(f"{len(error_list)+1}. Invalid airport name.")
      # ------All fields check complete--------#
      if len(error_list) > 0:
        error_message = ""
        for error in error_list:
          error_message += error
          error_message += "\n"
        messagebox.showerror(parent=update_window,
                             title="Error",
                             message="Invalid data input",
                             detail=error_message)
      # if all values qualify, update to table.
      else:
        # ask user to double check inputs
        confirm = messagebox.askyesno(
            parent=update_window,
            title="Confirm Submission",
            message=
            "Please check that all data inputs are correct. Confirm submission?"
        )

        if confirm:

          # fetch all input values and update into Pilot Table
          destination_id = entry_dict["DestinationID"].get().upper()
          destination_airport = entry_dict["DestinationAirport"].get().title()
          city = entry_dict["City"].get().title()
          country = entry_dict["Country"].get().title()
          timezone = entry_dict["Timezone"].get()

          c.execute(
              '''
              update INTO DESTINATIONS VALUES 
              (?, ?, ?, ?, ?)
              ''', (destination_id,
                    None if destination_airport == "" else destination_airport,
                    None if city == "" else city,
                    None if country == "" else country,
                    None if timezone == "" else timezone))
          conn.commit()
          # show messagebox confirming updateion
          messagebox.showinfo(parent=update_window,
                              title="Success",
                              message="Record updateed!")

      # background colour back to white

    # -----------------FLIGHTS------------------#
    if table_dropdown.get() == "Flights":

      # list of all error messages to display
      error_list = []

      # Unique Primary Key
      c.execute('''select FlightID from Flights''')
      flightIDs = c.fetchall()
      key_values = [flightID[0] for flightID in flightIDs]
      if entry_dict["FlightID"].get() in key_values:
        error_list.append(
            f"{len(error_list)+1}. FlightID already exist in record. Primary key cannot have duplicate values."
        )

      if entry_dict["FlightID"].get() == "":
        error_list.append(f"{len(error_list)+1}. FlightID cannot be empty.")

      if not re.match(r'^[a-zA-Z0-9]{5}$', entry_dict['FlightID'].get()):
        error_list.append(
            f"{len(error_list)+1}. FlightID must be 5-digit code consisting of only letters A-Z and numbers 0-9."
        )
      # ADD CHECK FOR FOREIGN KEYS

      # airport code check
      # check foreign key validity for DepartureAirport and ArrivalAirport fields
      c.execute('''select DestinationID from Destinations''')
      destinationIDs = c.fetchall()
      destinationID_existing = [
          destinationID[0] for destinationID in destinationIDs
      ]

      if entry_dict["DepartureAirport"].get() != "" and entry_dict[
          "DepartureAirport"].get() not in destinationID_existing:
        error_list.append(
            f"{len(error_list)+1}. Invalid Departure airport, please add new destination airport before assigning to flight."
        )
      if entry_dict["ArrivalAirport"].get() != "" and entry_dict[
          "ArrivalAirport"].get() not in destinationID_existing:
        error_list.append(
            f"{len(error_list)+1}. Invalid Arrival airport, please add new destination airport before assigning to flight."
        )

      # check foreign key validity for aircraftID field
      c.execute('''select AircraftID from Aircrafts''')
      aircraftIDs = c.fetchall()
      aircraftID_existing = [aircraftID[0] for aircraftID in aircraftIDs]

      if entry_dict["AircraftID"].get() != "" and entry_dict["AircraftID"].get(
      ) not in aircraftID_existing:
        error_list.append(
            f"{len(error_list)+1}. Invalid AirportID, please add aircraft before assigning to flight."
        )
      # Name must be String of text (letters in the alphabet)
      if entry_dict["FlightDuration"].get() != "" and not re.match(
          r'^\d{1,2}h\d{1,2}m$', entry_dict["FlightDuration"].get()):
        error_list.append(
            f"{len(error_list)+1}. Flight duration must be in 'xxhxxm' format, e.g. 08h55m."
        )

      if entry_dict["DepartureDate"].get() != "" and not re.match(
          r'^\d{4}-\d{2}-\d{2}$', entry_dict["DepartureDate"].get()):
        error_list.append(
            f"{len(error_list)+1}. DepartureDate must be in 'YYYY-MM-DD' format."
        )

      if entry_dict["DepartureTime"].get() != "" and not re.match(
          r'^(?:[01]\d|2[0-3]):[0-5]\d$', entry_dict["DepartureTime"].get()):
        error_list.append(
            f"{len(error_list)+1}. DepartureTime must be in 'HH:MM' format.")

      # ------All fields check complete--------#
      if len(error_list) > 0:
        error_message = ""
        for error in error_list:
          error_message += error
          error_message += "\n"
        messagebox.showerror(parent=update_window,
                             title="Error",
                             message="Invalid data input",
                             detail=error_message)
      # if all values qualify, update to table.
      else:
        # ask user to double check inputs
        confirm = messagebox.askyesno(
            parent=update_window,
            title="Confirm Submission",
            message=
            "Please check that all data inputs are correct. Confirm submission?"
        )
        if confirm:
          # fetch all input values and update into Pilot Table
          flight_id = entry_dict["FlightID"].get().upper()
          departure_airport = entry_dict["DepartureAirport"].get().upper()
          arrival_airport = entry_dict["ArrivalAirport"].get().upper()
          aircraft_id = entry_dict["AircraftID"].get().upper()
          if entry_dict["AircraftID"].get() != '':
            flight_duration_h = int(
                entry_dict["FlightDuration"].get().split("h")[0])
            flight_duration_m = int(entry_dict["FlightDuration"].get()[-3:-1])
            flight_duration = flight_duration_h * 60 + flight_duration_m
          else:
            flight_duration = -1
          departure_date = entry_dict["DepartureDate"].get()
          departure_time = entry_dict["DepartureTime"].get() + ":00"
          type = entry_dict["Type"].get()

          c.execute(
              '''
              update INTO FLIGHTS VALUES 
              (?, ?, ?, ?, ?, ?, ?, ?)
              ''', (flight_id,
                    None if departure_airport == "" else departure_airport,
                    None if arrival_airport == "" else arrival_airport,
                    None if aircraft_id == "" else aircraft_id,
                    None if flight_duration == -1 else flight_duration,
                    None if departure_date == "" else departure_date,
                    None if departure_time == "" else departure_time,
                    None if type == "" else type))

          conn.commit()
          # show messagebox confirming updateion
          messagebox.showinfo(parent=update_window,
                              title="Success",
                              message="Record updateed!")

          # fetch all listbox values and update to pilot-flight Junction table
          associated_pilots = [
              entry_dict['PilotID'].get(index)
              for index in entry_dict['PilotID'].curselection()
          ]

          if len(associated_pilots) > 0:
            for pilot_id in associated_pilots:
              c.execute(f'''
              update INTO Pilot_Flight_JUNC VALUES 
              ('{pilot_id}','{flight_id}')
              ''')
              conn.commit()

    # -----------------AIRCRAFTS------------------#

    if table_dropdown.get() == "Aircrafts":

      # list of all error messages to display
      error_list = []

      # Unique Primary Key
      c.execute('''select AircraftID from Aircrafts''')
      aircraftIDs = c.fetchall()
      key_values = [aircraftID[0] for aircraftID in aircraftIDs]
      if entry_dict["AircraftID"].get() in key_values:
        error_list.append(
            f"{len(error_list)+1}. AircraftID already exist in record. Primary key cannot have duplicate values."
        )

      if entry_dict["AircraftID"].get() == "":
        error_list.append(f"{len(error_list)+1}. AircraftID cannot be empty.")

      if not re.match(r'^[a-zA-Z0-9]{10}$', entry_dict['AircraftID'].get()):
        error_list.append(
            f"{len(error_list)+1}. AircraftID must be 10-digit code consisting of only letters A-Z and numbers 0-9."
        )

      # Other fields check
      if entry_dict["RegistrationNumber"].get() != "" and not re.match(
          r'^[a-zA-Z0-9]{8}$', entry_dict["RegistrationNumber"].get()):
        error_list.append(
            f"{len(error_list)+1}. RegistrationNumber must be 10-digit code consisting of only letters A-Z and numbers 0-9."
        )

      if entry_dict["ManufacturingDate"].get() != "" and not re.match(
          r'^\d{4}-\d{2}-\d{2}$', entry_dict["ManufacturingDate"].get()):
        error_list.append(
            f"{len(error_list)+1}. ManufacturingDate must be in 'YYYY-MM-DD' format."
        )

      if entry_dict["SeatingCapacity"].get() != "" and not re.match(
          r'^(?:[1-9]\d{0,2}|900)$', entry_dict["SeatingCapacity"].get()):
        error_list.append(
            f"{len(error_list)+1}. SeatingCapacity must be an integer in range 1-900."
        )

      if entry_dict["FuelCapacity"].get() != "" and not re.match(
          r'^(?:[1-9]\d{0,4}|100000)$', entry_dict["SeatingCapacity"].get()):
        error_list.append(
            f"{len(error_list)+1}. SeatingCapacity must be an integer in range 1-100,000."
        )

      if entry_dict["MaximumDistance"].get() != "" and not re.match(
          r'^(?:(?:[1-9]\d*|0)(?:\.\d{1,2})?)$',
          entry_dict["MaximumDistance"].get()):
        error_list.append(
            f"{len(error_list)+1}. MaximumDistance must be a positive number with maximum 2 decimals."
        )

      # ------All fields check complete--------#
      if len(error_list) > 0:
        error_message = ""
        for error in error_list:
          error_message += error
          error_message += "\n"
        messagebox.showerror(parent=update_window,
                             title="Error",
                             message="Invalid data input",
                             detail=error_message)
      # if all values qualify, update to table.
      else:
        # ask user to double check inputs
        confirm = messagebox.askyesno(
            parent=update_window,
            title="Confirm Submission",
            message=
            "Please check that all data inputs are correct. Confirm submission?"
        )
        if confirm:
          # fetch all input values and update into Pilot Table
          aircraft_id = entry_dict["AircraftID"].get().upper()
          model = entry_dict["Model"].get()
          registration_number = entry_dict["RegistrationNumber"].get().upper()
          manufacturer = entry_dict["Manufacturer"].get()
          manufacturing_date = entry_dict["ManufacturingDate"].get()
          seating_capacity = int(entry_dict["SeatingCapacity"].get(
          )) if entry_dict["SeatingCapacity"].get() != "" else -1
          engine_type = entry_dict["EngineType"].get()
          fuel_capacity = int(entry_dict["FuelCapacity"].get(
          )) if entry_dict["FuelCapacity"].get() != "" else -1
          maximum_distance = float(entry_dict["MaximumDistance"].get(
          )) if entry_dict["MaximumDistance"].get() != "" else -1
          ownership_type = entry_dict["OwnershipType"].get()
          insured = entry_dict["Insured"].get()

          c.execute(
              '''
              update INTO AIRCRAFTS VALUES 
              (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
              ''', (aircraft_id, None if model == "" else model,
                    None if registration_number == "" else registration_number,
                    None if manufacturer == "" else manufacturer,
                    None if manufacturing_date == "" else manufacturing_date,
                    None if seating_capacity == -1 else seating_capacity,
                    None if engine_type == "" else engine_type,
                    None if fuel_capacity == -1 else fuel_capacity,
                    None if maximum_distance == -1 else maximum_distance,
                    None if ownership_type == "" else ownership_type,
                    None if insured == "" else insured))
          conn.commit()
          # show messagebox confirming updateion
          messagebox.showinfo(parent=update_window,
                              title="Success",
                              message="Record updateed!")

    return

  # add event listener to dropdown list
  table_dropdown.bind("<<ComboboxSelected>>", show_fields_textbox)

  # add confirm button
  confirm_button = Button(update_window,
                          text="Confirm",
                          command=update_confirm)
  confirm_button.place(relx=0.92, rely=0.70, x=0, y=0, anchor=SE)

  # add table viewer button
  viewer_button = Button(update_window,
                         text="Table Viewer",
                         command=table_viewer,
                         height=1)
  viewer_button.place(x=350, y=18)

  conn.commit()

  return
