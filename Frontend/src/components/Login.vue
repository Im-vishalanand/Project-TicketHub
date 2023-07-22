<template>
  <div class="vue-tempalte">
    <form>
      <h3>Sign In</h3>

      <div class="form-group">
        <label>Email address</label>
        <input type="email" class="form-control form-control-lg" v-model="credentials.email" required />
      </div>

      <div class="form-group">
        <label>Password</label>
        <input type="password" class="form-control form-control-lg" v-model="credentials.password" required />
      </div>

      <button type="submit" class="btn btn-dark btn-lg btn-block">
        Sign In
      </button>

      <p class="forgot-password text-right mt-2 mb-4">
        <router-link to="/forgot-password">Forgot password ?</router-link>
      </p>

    </form>
  </div>
</template>

<script>

import axios from 'axios'
import Swal from 'sweetalert2'

export default {
  data() {
    return {
            credentials: {
                email: '',
                password: ''
            },
        };
  },
  methods: {
        login() {

            const endpoint = this.getEndpoint();
            axios.post(endpoint, this.credentials)
                .then(response => {
                    localStorage.setItem('credentials', JSON.stringify(response.data));
                    Swal.fire({
                        title: 'Success!',
                        text: 'Logged In Successfully !',
                        icon: 'success',
                        showConfirmButton: false, // Remove the 'OK' button
                        timer: 2000, // Set the timer for 2 seconds (adjust as needed)
                        willClose: () => {
                            window.location = '/'; // Redirect after the animation completes
                        }
                    });


                })
                .catch(error => {

                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: error.response.data.error,
                        confirmButtonText: 'Try again',
                        footer: '<a href="/">Go to home page</a>'
                    })

                    // alert("Error: " + error.response.data.error);
                });
        },
        getEndpoint() {
            return `http://localhost:5000/user/login`;
        },

    }
};





</script>

<style>

  input{
    margin-bottom: 10px;
  }
</style>
