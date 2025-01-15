
class LikeLogic:
    def _init_(self, dal):
        self.dal = dal
        ""

    def add_like(self, user_id, vacation_id):
        vacation = self.dal.get_vacation_by_id(vacation_id)
        if not vacation:
            raise ValueError("Vacation not found")
        user = self.dal.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        if user['role'] == 2:
            raise ValueError("Admins cannot like vacations")
        if self.dal.check_like_exists(user_id, vacation_id):
            raise ValueError("User has already liked this vacation")
        self.dal.add_like(user_id, vacation_id)
    "identify the vacation by her id if its not found wrote error,identify the user by his id if its not found wrote error"
    "check if the user is admin if he is wrote an error "
    "check if the user already did like to the vacation if he does wrote an error"
    "doing like to the vacation in the dal with the user id and the vacation id"
    def remove_like(self, user_id, vacation_id):
        if not self.dal.check_like_exists(user_id, vacation_id):
            raise ValueError("Like not found")
        self.dal.remove_like(user_id, vacation_id)
        "check if the like is existing if its not wrote an error if it does remove like in the dal"
    def get_user_likes(self, user_id):
        user = self.dal.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return self.dal.get_user_likes(user_id)
    "get the user id from the dal if the user id has not been found wrote an error else get user like from the dal"

    def check_like_exists(self, user_id, vacation_id):
        return self.dal.check_like_exists(user_id, vacation_id)
    "check in the dal if the user did like to the vacation "