class ContextManager {

  getCurrentHour() {
    return new Date().getHours();
  }

  getTimeContext() {

    const hour = this.getCurrentHour();

    if (hour >= 5 && hour < 12) {
      return "Morning";
    }

    if (hour >= 12 && hour < 17) {
      return "Afternoon";
    }

    if (hour >= 17 && hour < 21) {
      return "Evening";
    }

    return "Night";

  }

  calculateContextScore(category) {

    const time = this.getTimeContext();

    if (time === "Morning") {

      if (category === "Education") return 100;
      if (category === "Technology") return 90;
      if (category === "News") return 85;

    }

    if (time === "Afternoon") {

      if (category === "Technology") return 100;
      if (category === "Sports") return 90;
      if (category === "Business") return 85;

    }

    if (time === "Evening") {

      if (category === "Sports") return 100;
      if (category === "Entertainment") return 95;
      if (category === "Comedy") return 90;

    }

    if (time === "Night") {

      if (category === "Entertainment") return 100;
      if (category === "Music") return 95;
      if (category === "Movies") return 90;

    }

    return 50;

  }

}

export default new ContextManager();