# Answers to the Technical Questions

## Question 2

> How long did you spend on the coding test below?

It took me around 2 weeks to do what I have done so far.

> What would you add to your solution if you had more time? If you didn't spend much time on the coding test then use this as an opportunity to explain what you would add.

Being primarily a front-end dev, and coming from a React background, I am relatively new to Vue JS. But I guess I picked it up fast enough. Although I wasn't able to implement many features that I should have. I wasn't able to implement `vue-router` with django, therefore I haven't been able to make it an SPA. I also wished to utlize `vuetify` or `bootstrap`-like css frameworks, I couldn't. Therefore the application is not responsive. Error responses from APIs wasn't handled properly. I'm highly skilled with `Redux`, and for this project I've been planning on using `vuex` for state management. Eventually I couldn't afford the time to learn and utilize that.

On the back-end, I haven't included 'audit log' in the model. I would've implemented that.

Finally deployment, I still don't know what I missed. I did everything I could to deploy the app on AWS. [Please check out the deployed version of my app on the AWS](https://p8mpro6ohh.execute-api.us-east-1.amazonaws.com/dev/). Something went wrong with the APIs. They work well on Postman, but not from `axios`. This can't be an issue with the back-end since it's working fine on Heroku. Other than the APIs, everything seems to be working just fine.

## Question 3

> What was the most useful feature that was added to the latest version of your chosen language?

This question is a bit confusing to me. If we're talking about languages, there was no 'choice'. It was both python and javascript. If we're talking about the front-end frameworks, I'd usually choose React, but for this project I chose Vue.

For JS, I'd say the 'the most useful' features still would be the features that enable functional programming. More specifically, the `map`, `reduce`, `filter` and `forEach` methods.

> Please include a snippet of code that shows how you've used it.

```javascript
// src-vue/src/components/TableRow.vue

export default {
  methods: {
    transformCategory: function(str) {
      return str
        .split("_")
        .map(word => {
          let transformed = word.slice(0, 1).toUpperCase();
          if (word.length > 1) transformed += word.slice(1);
          return transformed;
        })
        .join(" ");
    }
  }
};
```

## Question 4

> How would you track down a performance issue in production? Have you ever had to do this?

No.
