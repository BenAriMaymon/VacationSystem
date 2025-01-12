from utils.dal import DAL
from logic.user_logic import UserLogic
from logic.vacation_logic import VacationLogic
from logic.like_logic import LikeLogic
from facade.system_facade import SystemFacade


class VacationManagementSystem:
    def __init__(self):
        self.dal = DAL()
        self.user_logic = UserLogic(self.dal)
        self.vacation_logic = VacationLogic(self.dal)
        self.like_logic = LikeLogic(self.dal)
        self.facade = SystemFacade(self.user_logic, self.vacation_logic, self.like_logic, self.dal)

    def display_menu(self):
        pass

    def register(self):
        pass

    def login(self):
        pass

    def add_vacation(self):
        pass

    def view_vacations(self):
        pass

    def handle_likes(self):
        pass

    def view_liked_vacations(self):
        pass

    def edit_vacation(self):
        pass

    def delete_vacation(self):
        pass
    def run(self):
        pass


if __name__ == "__main__":

    system = VacationManagementSystem()
    system.run()