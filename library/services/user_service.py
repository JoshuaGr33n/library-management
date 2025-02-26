from ..repositories.user_repository import UserRepository

class UserService:
    @staticmethod
    def get_all_users():
        return UserRepository.get_all()

    @staticmethod
    def get_user_by_id(user_id):
        return UserRepository.get_by_id(user_id)

    @staticmethod
    def create_user(**kwargs):
        return UserRepository.create(**kwargs)

    @staticmethod
    def update_user(user_id, **kwargs):
        user = UserRepository.get_by_id(user_id)
        if user:
            return UserRepository.update(user, **kwargs)
        return None

    @staticmethod
    def delete_user(user_id):
        user = UserRepository.get_by_id(user_id)
        if user:
            UserRepository.delete(user)
            return True
        return False
    
    
    @staticmethod
    def get_user_profile(user):
        return user

    @staticmethod
    def deactivate_user(user_id):
        user = UserRepository.get_by_id(user_id)
        if user:
            user.is_active = False
            user.save()
            return True
        return False

    @staticmethod
    def reactivate_user(user_id):
        user = UserRepository.get_by_id(user_id)
        if user:
            user.is_active = True
            user.save()
            return True
        return False 
    
    @staticmethod
    def update_user_password(user, new_password):
        user.set_password(new_password)
        user.save()
        
    @staticmethod
    def change_password(user, old_password, new_password):
        # Verify the old password
        if not user.check_password(old_password):
            raise ValueError("Old password is incorrect.")

        # Update the password
        UserService.update_user_password(user, new_password)    