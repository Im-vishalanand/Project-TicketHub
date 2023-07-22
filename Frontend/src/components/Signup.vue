<template>

  <div class="vue-tempalte">
    <form @submit.prevent="register">
      <h3>Sign Up</h3>

      <div class="form-group">
        <label>Email address</label>
        <input type="text" id="email" v-model="registerData.email" class="form-control form-control-lg" required/>
      </div>
      
      <div class="form-group">
        <label>Password</label>
        <input type="password" v-model="registerData.password" class="form-control form-control-lg" required/>
      </div>

      <div class="form-group">
        <label>Username</label>
        <input type="text" id="text" v-model="registerData.username" class="form-control form-control-lg" required/>
      </div>

      <div class="form-group">
        <label>Bio</label>
        <input type="text" id="text" v-model="registerData.bio" class="form-control form-control-lg" required />
      </div>
      
      <div class="form-group">
        <label>Membership Type</label>
        <input type="radio" id="regular" name="membershipType" value="regular" v-model="registerData.membership" >
        <label for="male">Regular</label>
        <input type="radio" id="premium" name="membershipType" value="premium" v-model="registerData.membership">
        <label for="css">Premium</label>
        <input type="radio" id="vip" name="membershipType" value="vip" v-model="registerData.membership">
        <label for="others">VIP</label>
      </div>
      
      <div class="form-group">
        <label>Gender</label>
        <input type="radio" id="male" name="gender" value="male" v-model="registerData.gender">
        <label for="male">Male</label>
        <input type="radio" id="female" name="gender" value="female" v-model="registerData.gender">
        <label for="css">Female</label>
    </div>

    <div class="form-group">
      <label for="dob">Date of Birth</label>
      <input type="date" id="dob"  :max="getCurrentDate()" v-model="registerData.dob" required>
    </div>

      <button v-on:click="register" type="submit" class="btn btn-dark btn-lg btn-block">Sign Up</button>
      
      <p class="forgot-password text-right">
        Already registered
        <router-link :to="{ name: 'login' }">sign in?</router-link>
      </p>
    </form>
  </div>
</template>

<script>

import axios from 'axios'
import Swal from 'sweetalert2';

export default {
  name: "Register",
    data() {
        return {
            registerData: {
              email: "",
              password: "",
              username: "",
              bio: "",
              membership: "",
              gender: "",
              dob: ""

            }
        };
    },
    methods: {
        register() {
          
          console.log('Register method called.');
          console.log(this.registerData.email);

            axios.post('http://127.0.0.1:5000/user/signup', this.registerData)
                .then(response => {
                    // Handle the response from the server
                    // Optionally, you can display a success message or redirect to a different page
                    console.log(this.registerData)
                    const registerId = response.data.register_id;

                    Swal.fire({
                        title: 'Sign Up Successful !',
                        text: "Added! with user ID " + registerId,
                        icon: 'success',
                        showConfirmButton: false, // Remove the 'OK' button
                        timer: 2000, // Set the timer for 2 seconds (adjust as needed)
                        willClose: () => {
                            window.location = '/'; // Redirect after the animation completes
                        }
                    });

                    // alert("Added! with guest ID "+ guestId)
                    // window.location = '/'
                })
                .catch(error => {
                    // Handle any errors that occurred during the registration process
                    // Optionally, you can display an error message to the user

                    Swal.fire({
                        icon: 'error',
                        title: 'Something Went Wrong...',
                        text: error,
                        footer: '<a href="">go to home page</a>'
                    })
                    // alert(error.response.data.error)
                });
        },
        getCurrentDate() {
            const today = new Date();
            const year = today.getFullYear() - 15;
            let month = today.getMonth() + 1;
            let day = today.getDate();

            if (month < 10) {
                month = `0${month}`;
            }
            if (day < 10) {
                day = `0${day}`;
            }

            return `${year}-${month}-${day}`;
        }
    }
};
</script>

<style>

input{
  margin-bottom: 10px;
}

#membershipType{
  margin-left: 50px;
  padding: 3px;
  font-size: 18px;
  margin-bottom: 10px;
  margin-top: 10px;
}

#male, #dob{
  margin-left: 70px;
  margin-top: 20px;
}

#female, #others, #regular, #premium, #vip{
  margin-left: 30px;
}

#regular, #premium, #vip{
  margin-top: 20px;
  margin-left: 5px;
}

#male~label, #regular~label, #female, #others{
  margin-left: 8px;
}

a{
  text-decoration: none;
}


</style>
