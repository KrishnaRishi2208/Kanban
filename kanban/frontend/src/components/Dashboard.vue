<template>
    <div>

  <nav class="navbar bg-light">
  <div class="container-fluid">
    <label class="navbar-brand" @click="gohome">Kanban App</label>
    <div class="d-flex" role="search">
        <button class="btn btn-outline-success" @click="createList">Create List</button>
        <button class="btn btn-outline-success" @click="logout(1)">Log Out</button>
    </div>
  </div>  
</nav>
<h2 style="text-decoration: underline;" >Welcome {{error}},</h2>
<div class="card2 text-center col-sm " style="width: 18rem;float:left;margin-right: 5%;" v-for="(value,key) in totdat">
  <div class="card-body">
    <div class="dropdown">
  <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
    {{key}}
  </button>
  <ul class="dropdown-menu">
    <li><a class="dropdown-item" @click="editlist(key)">Edit List</a>
    </li>
    <li><a class="dropdown-item" @click="deletelist(key)">Delete List</a></li>

  </ul>
</div>
<div class="card card1" v-for="data in value" style="background-color:{{colour}}">
  <div class="card-body">
    <div class="dropdown">
  <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false" style="margin-bottom:10%">
    {{data[0]}}
  </button>
  <ul class="dropdown-menu">
    <li><a class="dropdown-item" @click="editcard(key,data[0],data[1],data[2])">Edit Card</a></li>
    <li><a class="dropdown-item" @click="deletecard(key,data[0])">Delete Card</a></li>
    <li><a class="dropdown-item" @click="statcard(key,data[0])" v-if="data[3]==0">Mark As Complete</a></li>
    <li><a class="dropdown-item" @click="stat0card(key,data[0])" v-if="data[3]==1">Mark As Incomplete</a></li>
    <li>
      <a class="dropdown-item" href="#">
        Move Card&raquo;
      </a>
      <ul class="dropdown-menu dropdown-submenu">
        <div v-for="(value,key2) in totdat">
        <li>
          <a class="dropdown-item" @click="movecard(key,key2,data[0])" v-if="key!=key2">{{key2}}</a>
        </li>
      </div>
      </ul>
    </li>


  </ul>
  <p>{{data[1]}}</p>
  <p>Expiry date: {{data[2]}}</p>
  <p v-if="data[3]==1" style="color:aquamarine">Completed</p>
  <p></p>
</div>
  </div>
</div>
<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-plus-circle" viewBox="0 0 16 16" @click="addcard(key)" style="margin-top:10%">
  <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
  <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
</svg>
<br>
    <a  class="btn btn-success" style="margin-top:10%" @click="exportlist(key)">Export</a>
  </div>
</div>
</div>
</template>

<script>
// Functions first

export default {
    data() {
    return {
      error:'',
      id:'',
      totdat:'',
      colour:'green'
    }
  },


    created(){
        this.id=this.$route.params.id
        const url = `http://192.168.0.105:8080/getauth/${this.id}`;
            fetch(url,{
                method:"GET"
    })
    .then(resp=> resp.json())
    .then(data => {
        this.error=this.id
      if (data.auth=="False"){
        this.$router.push('/')
      }
    });

    const url2=`http://192.168.0.105:8080/getlist/${this.id}`
    fetch(url2,{
                method:"GET"
    })
    .then(resp=> resp.json())
    .then(data => {
        this.totdat=data;
    });
        
    },
    methods:{
    createList(){
        let id=this.$route.params.id
        this.$router.push(`/createlist/${id}`)
    },
    gohome(){
        window.location.reload()
        let id=this.$route.params.id
        this.$router.push(`/dashboard/${id}`)
        
    },
    editlist(key){
      let id=this.$route.params.id
      this.$router.push(`/editlist/${key}/${id}`)

    },
    deletelist(key){
    let id=this.$route.params.id 
    const url3=`http://192.168.0.105:8080/deletelist/${id}/${key}`
    fetch(url3,{
                method:"GET"
    })
    .then(resp=> resp.json())
    .then(data => {
        console.log('deleted list')
        this.gohome();
    });
    },
    editcard(key,cardname,cardsum,carddate){
      let id=this.$route.params.id
      this.$router.push(`/editcard/${id}/${key}/${cardname}/${carddate}/${cardsum}`)
    },
    deletecard(key,cardname){
    let id=this.$route.params.id 
    const url3=`http://192.168.0.105:8080/deletecard/${id}/${key}/${cardname}`
    fetch(url3,{
                method:"GET"
    })
    .then(resp=> resp.json())
    .then(data => {
        console.log('deleted list')
        this.gohome();
    });
    },
    statcard(key,cardname){
    let id=this.$route.params.id 
    const url3=`http://192.168.0.105:8080/stat1card/${id}/${key}/${cardname}`
    fetch(url3,{
                method:"GET"
    })
    .then(resp=> resp.json())
    .then(data => {
        console.log('updated card')
        this.gohome();
    });
    },
    stat0card(key,cardname){
    let id=this.$route.params.id 
    const url3=`http://192.168.0.105:8080/stat0card/${id}/${key}/${cardname}`
    fetch(url3,{
                method:"GET"
    })
    .then(resp=> resp.json())
    .then(data => {
        console.log('updated card')
        this.gohome();
    });
    },
    movecard(key,key2,cardname){
      let id=this.$route.params.id 
    const url3=`http://192.168.0.105:8080/movecard/${id}/${key}/${key2}/${cardname}`
    fetch(url3,{
                method:"GET"
    })
    .then(resp=> resp.json())
    .then(data => {
        console.log('updated card')
        this.gohome();
    });
    },
    addcard(key){
      let id=this.$route.params.id
      this.$router.push(`/addcard/${key}/${id}`)
    },
    logout(key){
    let id=this.$route.params.id 
    const url3=`http://192.168.0.105:8080/logout/${id}`
    fetch(url3,{
                method:"GET"
    })
    .then(resp=> resp.json())
    .then(data => {
        console.log('Logged out')
        this.gohome();
    });
    },
  }
}
</script>



<style>
.card1{
    background: var(--color-background);
    padding: calc(4 * var(--size-bezel));
    margin-top: calc(4 * var(--size-bezel));
    border-radius: var(--size-radius);
    border: 3px solid var(--color-shadow, currentColor);
}
.dropdown-menu li {
position: relative;
}
.dropdown-menu .dropdown-submenu {
display: none;
position: absolute;
left: 100%;
top: -7px;
}
.dropdown-menu .dropdown-submenu-left {
right: 100%;
left: auto;
}
.dropdown-menu > li:hover > .dropdown-submenu {
display: block;
}

</style>