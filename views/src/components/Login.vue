
<template>
    <!-- Log in -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/3.0.2/normalize.css"/>
    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">
    <div class="login">
        <form action="">
            <div class ="money-icon"><img src="@/assets/moneyBag.svg" alt="icono" class="icono"/></div>
            <h1><span>FinanceWebApp</span> Log in.</h1>

        <div class="input-container">
            <span class="icon"><i class="fa fa-at"></i></span>
            <input type="text" placeholder="Email"/>
        </div>

        <div class="input-container">
            <span class="icon"><i class="fa fa-lock"></i></span>
            <input type="password" placeholder="Password"/>
        </div>

        <div class="submit-row">
            <input type="submit" value="Log in &raquo;"/>
            <span class="reset">or <a href="#">Sign up</a></span>
        </div>
    </form>
</div>         
   
</template>

<script setup>

</script>

<style scoped>
 @import url(https://fonts.googleapis.com/css?family=Open+Sans);
    @import url(https://fonts.googleapis.com/css?family=Roboto:400,500);

.money-icon {
    display: flex;
    justify-content: center; 
    align-items: center; 
}
.icono{
width: 50px;
height: 60px;
}
.login{
    margin:100px auto;
    width:350px;
    max-height: 500px;
}


form h1{
    color:#dedede;
    font-size:2.8em;
    font-weight: normal;
    letter-spacing: -1px;
    font-family: Roboto;
}

form h1 span{
    font-weight: 500;
    letter-spacing: -1px;
    
}

form input{
    border:none;
    margin:0;
}

form .input-container{
    margin:2em 0;
    overflow:hidden;
}

form .icon{
    font-size:1.4em;
    background:#dacccc;
    padding:0.8em;
    border-left:4px solid #ea4c88;
    color:#1d1717;
    float:left;
}

form input[type="text"],form input[type="password"] {
    padding:0.8em 0.8em 0.8em 0;
    font-size:1.4em;
    color:#1b1717;
    width:275px;
}

form input[type="text"]:focus,form input[type="password"]:focus {
    outline:0;
}

form input[type="submit"]{
    border:none;
    background:#ea4c88;
    color:#FFFFFF;
    font-size:1.6em;
    padding:0.7em 1.2em;
    opacity: 1;
    transition: opacity .5s ease-in-out;
    -moz-transition: opacity .5s ease-in-out;
    -webkit-transition: opacity .5s ease-in-out;
    -webkit-border-radius: 2px;
    -moz-border-radius: 2px;
    border-radius: 2px;
}

form input[type="submit"]:hover {
    background:#c62a65;
    opacity: 0.8;
}

form .reset{
    margin-left:1em;
    color:#FFFFFF;
    font-size: 1.4em;
}

form .reset a{
    color:#FFFFFF;
}

form .reset a:hover{
    text-decoration: none;
}
</style>