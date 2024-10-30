<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      error: null, 
    };
  },
  methods: {
    async handleSubmit() {
      try {
        const response = await fetch('/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: this.username, password: this.password })
        });
        
        if (!response.ok) {
          const errorData = await response.json();
          this.error = errorData.error;
        } else {
          const data = await response.json();
          alert(data.message);
          this.error = null;
        }
      } catch (error) {
        this.error = 'Ocurrió un error al intentar iniciar sesión';
      }
    }
  }
};
</script>
