A parking garage: drivers take a numbered `GarageTicket` on entry (entry epoch recorded).
Shops validate tickets (validator capability). On exit a validated ticket leaves free — the
payment presented is returned untouched — while an unvalidated ticket pays the hourly rate
times epochs elapsed out of the presented payment, change returned. Fees pool for the
operator (capability) to sweep.
