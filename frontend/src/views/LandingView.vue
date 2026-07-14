<template>
  <div class="landing-page">
    <div class="content">
      <h1>Placement Portal Appication</h1>
      <p class="subtitle">Select your portal to continue</p>

      <div class="cards">
        <div class="card" @click="$router.push('/admin')">
          <h2>Admin</h2>
          <p>Manage students, companies and placement drives.</p>
        </div>

        <div class="card" @click="$router.push('/company')">
          <h2>Company</h2>
          <p>Create placement drives, manage applications and recruit students.</p>
        </div>

        <div class="card" @click="$router.push('/student')">
          <h2>Student</h2>
          <p>Browse placement drives, apply for opportunities and indulge in recruitment processes.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LandingView",
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.landing-page {
  height: 100vh;
  width: 100%;
  background: #efe7ff;
  display: flex;
  justify-content: center;
  align-items: center;
}

.content {
  width: 1100px;
  text-align: center;
}

h1 {
  font-size: 48px;
  color: #5b2ca0;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 18px;
  color: #555;
  margin-bottom: 60px;
}

.cards {
  display: flex;
  justify-content: space-between;
  gap: 40px;
}

.card {
  flex: 1;
  height: 320px;
  background: white;
  border-radius: 15px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.15);
  cursor: pointer;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  transition: 0.3s;
}

.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 30px rgba(0,0,0,0.25);
}

.card h2 {
  color: #5b2ca0;
  font-size: 30px;
  margin-bottom: 20px;
}

.card p {
  width: 80%;
  color: #666;
  font-size: 16px;
  line-height: 1.6;
}
</style>