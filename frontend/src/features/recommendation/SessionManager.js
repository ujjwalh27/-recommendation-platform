class SessionManager {

    constructor() {

        this.sessionVideos = 0;

    }

    incrementSession() {

        this.sessionVideos++;

    }

    getSessionCount() {

        return this.sessionVideos;

    }

    getSessionScore() {

        if (this.sessionVideos < 5)
            return 0;

        if (this.sessionVideos < 10)
            return 10;

        if (this.sessionVideos < 20)
            return 20;

        if (this.sessionVideos < 30)
            return 30;

        return 40;

    }

    resetSession() {

        this.sessionVideos = 0;

    }

}

export default new SessionManager();