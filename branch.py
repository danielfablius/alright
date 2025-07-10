import datetime


class BackofficeBranch:
    def __init__(self, company_id, branch_id, cookiesession1, csrf_cookie_mpos, ci_session):
        self.company_id = company_id
        self.branch_id = branch_id
        self.cookiesession1 = cookiesession1
        self.csrf_cookie_mpos = csrf_cookie_mpos
        self.ci_session = ci_session
    
    def get_cookies(self):
        return {
            'csrf_cookie_mpos': self.csrf_cookie_mpos,
            'cookiesession1': self.cookiesession1,
            'ci_session': self.ci_session,
        }


class Branch:
    def __init__(self, company_ids, branch_ids, name, cookiesession1s, csrf_cookie_mposs, ci_sessions, target, whatsapp_group_name, opening_hour, closing_hour=3, default_targets=None):
        self.company_ids = company_ids
        self.branch_ids = branch_ids
        self.name = name
        self.backoffices = [BackofficeBranch(company_ids[x], branch_ids[x], cookiesession1s[x], csrf_cookie_mposs[x], ci_sessions[x]) for x in range(len(branch_ids))]
        self.target = target
        self.default_targets = default_targets
        self.whatsapp_group_name = whatsapp_group_name
        self.opening_hour = opening_hour
        self.closing_hour = closing_hour
    
    def get_target(self, grand_total):
        if self.default_targets is not None:
            self.target = self.default_targets[datetime.datetime.weekday(self.get_shifting_date())]
            
        if grand_total > self.target:
            self.target = 50 * ((grand_total // 50) + 1)
        
        return self.target
    
    def get_shifting_date(self): 
        # Shifting Date will be set to yesterday when the current hour is between
        # midnight and Closing Hour (1 hour before opening hour of each branch).
        now = datetime.datetime.now()

        if now.hour < self.opening_hour - 1:
            return now - datetime.timedelta(1)
        else:
            return now
    
    def get_start_date(self):
        # Start Date will be set to current shifting date,
        return self.get_shifting_date()
    
    def get_start_date_string(self):
        return self.get_start_date().strftime('%d/%m/%Y')

    def get_end_date(self):
        # while the End Date will be the next day.
        return self.get_shifting_date() + datetime.timedelta(1)
    
    def get_end_date_string(self):
        return self.get_end_date().strftime('%d/%m/%Y')
    
    def get_start_time(self):
        # Start Time will be set to Opening Hour of the shifting date,
        return self.get_start_date().replace(hour=self.opening_hour, minute=0, second=0).strftime('%H:%M')
    
    def get_end_time(self):
        # while the End Time will always be set to an hour before Opening Hour of end_date.
        return self.get_end_date().replace(hour=self.opening_hour - 1, minute=0, second=0).strftime('%H:%M')
    