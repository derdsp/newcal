import ephem
import datetime
from icalendar import Calendar, Event

def generate_focus_calendar(start_year, end_year):
    cal = Calendar()
    cal.add('prodid', '-//Kosmos Fokus//DE')
    cal.add('version', '2.0')
    cal.add('X-WR-CALNAME', 'Mond-Zyklus (Fokus)')
    cal.add('METHOD', 'PUBLISH')

    # Die Namen der 12 Monde
    months = [
        "Isannos (Eismond)", "Anuanda (Keimmond)", "Blutios (Blütenmond)", 
        "Giamon (Saatmond)", "Simivisonna (Wachstumsmond)", "Equos (Heumond)", 
        "Aedon (Glutmond)", "Messos (Erntemond)", "Vindos (Taumond)", 
        "Dulon (Nebelmond)", "Samonios (Frostmond)", "Dumnos (Dunkelmond)"
    ]

    for year_val in range(start_year, end_year + 1):
        # 1. Astronomische Ankerpunkte
        ws_prev = ephem.next_solstice(f'{year_val-1}/12/20')
        ws_current = ephem.next_solstice(f'{year_val}/12/20')
        
        # 2. Neumonde mit Monatsnamen verknüpfen
        # Wir suchen den ersten Neumond nach der Wintersonnenwende
        curr_nm_date = ephem.next_new_moon(ws_prev)
        
        for i in range(12):
            nm_dt = curr_nm_date.datetime().date()
            if nm_dt >= ws_current.datetime().date():
                break
                
            m_name = months[i]
            
            # Event für Neumond + Monatsbeginn
            e_nm = Event()
            e_nm.add('summary', f'🌑 Neumond: Beginn {m_name}')
            e_nm.add('dtstart', nm_dt)
            e_nm.add('dtend', nm_dt + datetime.timedelta(days=1))
            e_nm.add('description', f'Ein neuer kosmischer Zyklus beginnt. Fokus: {m_name}.')
            cal.add_component(e_nm)
            
            # 3. Anam (Zwischenstille) nach dem 28. Tag dieses Mondes
            # Der 28. Tag ist 27 Tage nach dem Start
            anam_start = nm_dt + datetime.timedelta(days=28)
            next_nm_date = ephem.next_new_moon(curr_nm_date)
            next_nm_dt = next_nm_date.datetime().date()
            
            # Tage zwischen Tag 28 und dem nächsten Neumond füllen
            temp_date = anam_start
            while temp_date < next_nm_dt and temp_date < ws_current.datetime().date():
                e_anam = Event()
                e_anam.add('summary', '✨ Anam (Atempause)')
                e_anam.add('dtstart', temp_date)
                e_anam.add('dtend', temp_date + datetime.timedelta(days=1))
                e_anam.add('description', f'Zwischenstille nach dem {m_name}.')
                cal.add_component(e_anam)
                temp_date += datetime.timedelta(days=1)
                
            # Zum nächsten Neumond springen
            curr_nm_date = next_nm_date

        # 4. Vollmonde (als reine Energiepunkte)
        date_cursor = ws_prev
        while date_cursor < ephem.next_solstice(f'{year_val}/12/25'):
            fm = ephem.next_full_moon(date_cursor)
            fm_dt = fm.datetime().date()
            if fm_dt.year == year_val:
                e_fm = Event()
                e_fm.add('summary', '🌕 Vollmond (Kraft & Fülle)')
                e_fm.add('dtstart', fm_dt)
                e_fm.add('dtend', fm_dt + datetime.timedelta(days=1))
                cal.add_component(e_fm)
            date_cursor = fm + 1

        # 5. Gwylnos (Weltenruhe)
        gwyl_start = ws_current.datetime().date()
        gwyl_end = ephem.next_new_moon(ws_current).datetime().date()
        temp_date = gwyl_start
        while temp_date < gwyl_end:
            e_gwyl = Event()
            e_gwyl.add('summary', '🌌 Gwylnos (Weltenruhe)')
            e_gwyl.add('dtstart', temp_date)
            e_gwyl.add('dtend', temp_date + datetime.timedelta(days=1))
            cal.add_component(e_gwyl)
            temp_date += datetime.timedelta(days=1)

    with open("mond_zyklus_live.ics", "wb") as f:
        f.write(cal.to_ical())
    print("Der ewige Fokus-Kalender wurde mit Monatsnamen erstellt!")

if __name__ == "__main__":
    generate_focus_calendar(2026, 2031)