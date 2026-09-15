class User:
    def __init__(self, name, gender, password):
        self.name = name
        self.gender = gender
        self.__password = password  # Atributo privado
        self.posts = []            # Relación: Un usuario tiene una lista de sus publicaciones

    def following(self):
        print(f'Someone started following {self.name}')

    def show_profile(self):
        print(f'Name: {self.name}')
        print(f'Gender: {self.gender}')
        print(f'Total posts: {len(self.posts)}')

    # Relación: Crear post y asociarlo automáticamente al usuario
    def create_post(self, media, date):
        new_post = Post(media=media, date=date, author=self)
        self.posts.append(new_post)
        print(f'{self.name} created a new post!')
        return new_post

    # Relación: El usuario envía un mensaje directo a otro usuario
    def send_dm(self, receiver, message_text, date):
        new_dm = DM(message=message_text, sender=self, receiver=receiver, date=date)
        new_dm.send_message()
        return new_dm


class Post:
    def __init__(self, media, date, author, likes=0):
        self.media = media
        self.likes = likes
        self.date = date
        self.author = author      # Relación: Cada post conoce a su creador (User)
        self.comments = []        # Relación: Un post tiene una lista de comentarios

    def show_post(self):
        print(f'\n--- POST by {self.author.name} ---')
        print(f'Media: {self.media}')
        print(f'Likes: {self.likes}')
        print(f'Date: {self.date}')
        print(f'Comments count: {len(self.comments)}')

    # Relación: Un usuario agrega un comentario a esta publicación
    def add_comment(self, user, comment_text):
        new_comment = Comment(comment=comment_text, user=user)
        self.comments.append(new_comment)
        print(f'{user.name} commented on {self.author.name}\'s post.')
        return new_comment

    def show_comments(self):
        print(f'\nComments on post ({self.media}):')
        for idx, c in enumerate(self.comments, 1):
            print(f'  {idx}. {c.user.name}: "{c.comment}" (Likes: {c.likes})')


class Comment:
    def __init__(self, comment, user, likes=0):
        self.comment = comment
        self.user = user  # Relación: Guarda el objeto User que escribió el comentario
        self.likes = likes

    def like(self):
        self.likes += 1
        print(f'Comment by {self.user.name} now has {self.likes} likes.')


class DM:
    def __init__(self, message, sender, receiver, date):
        self.message = message
        self.sender = sender      # Relación: Objeto User que envía el mensaje
        self.receiver = receiver  # Relación: Objeto User que recibe el mensaje
        self.date = date

    def show_message(self):
        print(f'\n--- DIRECT MESSAGE ---')
        print(f'From: {self.sender.name}')
        print(f'To: {self.receiver.name}')
        print(f'Message: {self.message}')
        print(f'Date: {self.date}')

    def send_message(self):
        print(f'Message sent from {self.sender.name} to {self.receiver.name}')

        #