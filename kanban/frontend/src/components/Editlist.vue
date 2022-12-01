<template>
    <div>
      <nav class="navbar bg-light">
    <div class="container-fluid">    <label class="navbar-brand" @click="gohome">Kanban App</label>   
      <form class="d-flex" role="search">
          <button class="btn btn-outline-success" @click="createList">Create List</button>
        <button class="btn btn-outline-success" type="submit">Log Out</button>
      </form>
    </div>
  </nav>
  <div>
      <form method="POST" @submit.prevent="verifyUser">
  
  <div id="app">
      <div class="card2 card--accent">
          <h2>Editing List</h2>
          <label class="input">
              NAME:
              <input class="input__field" type="text" title="email" name="email" v-model="lname" placeholder="{{lname}}" />
              <h1></h1>
          </label>
        
          <div class="button-group">
              <button type="submit" @click="next" >Submit</button>
          </div>
        </div>
      </div>
      <div class="alert alert-primary" role="alert" v-if="error">
          List couldnt be Edited, Try again
  </div>
  
  </form>
  </div>
    </div>
  </template>
  
  <script>
  export default {
      data() {
      return {
        lname:'',
        error:false,
        id:'',
        flname:''
      }
    },
  
      created(){
          // this.$router.go(0);
          this.id=this.$route.params.id
          const url = `http://192.168.0.105:8080/getauth/${this.id}`;
              fetch(url,{
                  method:"GET"
      })
      .then(resp=> resp.json())
      .then(data => {
        if (data.auth=="False"){
          this.$router.push('/')
        }
      });
      this.lname=this.$route.params.lname
      this.flname=this.$route.params.lname
      
          
      },
      methods:{
      createList(){
          let id=this.$route.params.id
          this.$router.push(`/createlist/${id}`)
      },
      next(){
          let id=this.$route.params.id
          const url = `http://192.168.0.105:8080/editlist/${id}/${this.flname}/${this.lname}`;
          fetch(url,{
                  method:"GET"
      })
      .then(resp=> resp.json())
      .then(data => {
        if (data.commit=="True"){
            let id=this.$route.params.id
          this.$router.push(`/dashboard/${id}`)
        }
        else{
          this.error=true
        }
      });
      },
      gohome(){
          let id=this.$route.params.id
          this.$router.push(`/dashboard/${id}`)
          
      }
    }
  }
  </script>
  
  <style>
  
  </style>