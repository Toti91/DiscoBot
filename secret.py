class Secret:
    token = "Your Discord bot token"
    gKey = "Your GIPHY API key"
    me = "Your discord user id"
    twitch = "Your Twitch API key"
    movies = "Your kvikmyndir.is API password"
    redditData = {"clientId": "Your Reddit client ID",
                "clientSecret": "Your Reddit client secret",
                "password": "Your Reddit password",
                "username": "Your Reddit username",
                "userAgent": "Your Reddit useragent"}
    afk = "Your AFK channel ID (Channel to kick users to)"

    def getToken(self):
        return self.token

    def getGiphyKey(self):
        return self.gKey

    def getRedditInfo(self):
        return self.data

    def getMe(self):
        return self.me

    def getTwitchKey(self):
        return self.twitch

    def getMoviePw(self):
        return self.movies

    def getAfkChannel(self):
        return self.afk

