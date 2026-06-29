const events = [];

const listeners = [];

const BehaviourTracker = {

  record(event) {

    events.unshift(event);

    listeners.forEach(listener => listener([...events]));

  },

  subscribe(listener) {

    listeners.push(listener);

  },

  unsubscribe(listener) {

    const index = listeners.indexOf(listener);

    if (index !== -1) {

      listeners.splice(index,1);

    }

  },

  getEvents() {

    return events;

  }

};

export default BehaviourTracker;