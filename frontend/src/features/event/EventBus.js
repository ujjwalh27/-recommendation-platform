class EventBus {

    constructor() {
        this.listeners = {};
    }

    subscribe(eventName, listener) {

        if (!this.listeners[eventName]) {
            this.listeners[eventName] = [];
        }

        this.listeners[eventName].push(listener);
    }

    unsubscribe(eventName, listener) {

        if (!this.listeners[eventName]) return;

        this.listeners[eventName] =
            this.listeners[eventName].filter(
                l => l !== listener
            );
    }

    publish(eventName, payload) {

        if (!this.listeners[eventName]) return;

        this.listeners[eventName].forEach(listener =>
            listener(payload)
        );
    }

}

export default new EventBus();