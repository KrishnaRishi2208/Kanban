const app = Vue.createApp({
  template: ``,
  data() {
    return {
      email: 'Rishi',
      password: 'Rishi',
    };
  },
  mounted() {
    const url = `http://192.168.0.105:8080/${this.email}/${this.password}`;
    fetch(url,{
      method:"GET"
    })
    .then(resp=> resp.json())
    .then(data => {
      this.email=data.auth
    });
  },
});

app.mount('#app');
