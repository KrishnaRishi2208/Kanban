<template>
    <div>
        <br>
        <br>
    <h2 style="text-align:center">Simple Kanban</h2>
    <form method="POST" @submit.prevent="verifyUser">

<div id="app3">
    <div class="card2 card--accent">
        <h2>Login Page</h2>
        <label class="input">
            
            <input class="input__field" type="text" title="email" name="email" v-model="email" placeholder="Username/Email" />
            <h1></h1>
            <input class="input__field" type="text" title="password" name="password" v-model="password" placeholder="Password" />
        </label>
      
        <div class="button-group">
            <button type="submit" @click="check" >Submit</button>

            <button @click="newuser" >Create New User</button>
        </div>
        <h3>{{error}}</h3>
      </div>
    </div>

</form>
</div>

</template>

<script>

export default {
    data() {
    return {
      email: '',
      password: '',
      error:'',
    }
  },
  methods:{
    verifyUser(){
        if (!this.email || !this.password){
            this.error="Please fill all feilds"
        }
        else{
            const url = `http://192.168.0.105:8080/login/${this.email}/${this.password}`;
            fetch(url,{
                method:"GET"
    })
    .then(resp=> resp.json())
    .then(data => {
      if (data.auth=="False"){
        this.error="Incorrect password"
      }
      else{
        this.$router.push(`/dashboard/${this.email}`) 
      }
    });
        }
    },
    newuser(){
      this.$router.push(`/newuser`) 
      
    }
  }

}
</script>

<style>

#app3 {
    width: 400px;
    height: 100vh;
    margin: auto;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
  

  
  @import url('https://rsms.me/inter/inter.css');

  :root {
    --color-light: white;
    --color-dark: #212121;
    --color-signal: #fab700;
    
    --color-background: var(--color-light);
    --color-text: var(--color-dark);
    --color-accent: var(--color-signal);
    
    --size-bezel: .5rem;
    --size-radius: 4px;
    
    line-height: 1.4;
    
    font-family: 'Inter', sans-serif;
    font-size: calc(.6rem + .4vw);
    color: var(--color-text);
    background: var(--color-background);
    font-weight: 300;
    padding: 0 calc(var(--size-bezel) * 3);
  }
  
  h1, h2, h3 {
    font-weight: 900;
  }
  
  mark {
    background: var(--color-accent);
    color: var(--color-text);
    font-weight: bold;
    padding: 0 0.2em;
  }
  
  .card2 {
    background: var(--color-background);
    padding: calc(4 * var(--size-bezel));
    margin-top: calc(4 * var(--size-bezel));
    border-radius: var(--size-radius);
    border: 3px solid var(--color-shadow, currentColor);
    box-shadow: .5rem .5rem 0 var(--color-shadow, currentColor);
    
    /* &--inverted {
      --color-background: var(--color-dark);
      color: var(--color-light);
      --color-shadow: var(--color-accent);
    }
    
    &--accent {
      --color-background: var(--color-signal);
      --color-accent: var(--color-light);
      color: var(--color-dark);
    } */
    
    *:first-child {
      margin-top: 0;
    }
  }
  
  
  .input__field{
    box-sizing: border-box;
    display: block;
    width: 100%;
    border: 3px solid currentColor;
    padding: calc(var(--size-bezel) * 1.5) var(--size-bezel);
    color: currentColor;
    background: transparent;
    border-radius: var(--size-radius);
  }
  
  .button-group {
    margin-top: calc(var(--size-bezel) * 2.5);
  }
  
  button {
    color: currentColor;
    padding: var(--size-bezel) calc(var(--size-bezel) * 2);
    background: var(--color-accent);
    border: none;
    border-radius: var(--size-radius);
    font-weight: 900;
    
    &[type=reset]{
      background: var(--color-background);
      font-weight: 200;
    } 
  }
  
  button + button {
    margin-left: calc(var(--size-bezel) * 2);
  }
  
  .icon {
    display: inline-block;
    width: 1em; height: 1em;
    margin-right: .5em;
  }
  
  .hidden {
    display: none;
  }
  
  

</style>