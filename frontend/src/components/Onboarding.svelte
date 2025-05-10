<script lang="ts">
    // Steps data model
    const steps = [
      { title: "Connect Your Insurance", type: "insurance" },
      { title: "Upload Historical Doctor Data", type: "doctorData" },
      { title: "Connect Google Fit", type: "googleFit" },
      { title: "All Done!", type: "done" }
    ];
  
    let currentStep = 0;
    let insuranceConnected = false;
    let doctorDataUploaded = false;
    let googleFitConnected = false;
    let uploading = false;
  
    // Placeholder for backend logic
    async function handleInsuranceConnect() {
      // Simulate backend call
      insuranceConnected = false;
      uploading = true;
      await new Promise(r => setTimeout(r, 1000));
      insuranceConnected = true;
      uploading = false;
    }
  
    async function handleDoctorDataUpload(event) {
      // Simulate backend upload
      doctorDataUploaded = false;
      uploading = true;
      await new Promise(r => setTimeout(r, 1000));
      doctorDataUploaded = true;
      uploading = false;
    }
  
    async function handleGoogleFitConnect() {
      // Simulate backend call
      googleFitConnected = false;
      uploading = true;
      await new Promise(r => setTimeout(r, 1000));
      googleFitConnected = true;
      uploading = false;
    }
  
    function handleContinue() {
      if (currentStep < steps.length - 1) {
        currentStep += 1;
      }
    }
  
    function handleSkip() {
      if (currentStep < steps.length - 1) {
        currentStep += 1;
      }
    }
  
    // Optional: handle swipe/scroll navigation
    let startY = 0;
    function handleTouchStart(e) {
      startY = e.touches[0].clientY;
    }
    function handleTouchEnd(e) {
      const endY = e.changedTouches[0].clientY;
      if (startY - endY > 50) handleContinue(); // swipe up
      if (endY - startY > 50 && currentStep > 0) currentStep -= 1; // swipe down
    }
  </script>
  
  <div
    class="onboarding-outer"
    on:touchstart={handleTouchStart}
    on:touchend={handleTouchEnd}
  >
    <div class="onboarding-container">
      <div class="onboarding-title">{steps[currentStep].title}</div>
      <div class="onboarding-content">
        {#if steps[currentStep].type === 'insurance'}
          <div class="square-placeholder">
            {#if insuranceConnected}
              <div>Insurance Connected!</div>
            {:else}
              <button class="action-btn" on:click={handleInsuranceConnect} disabled={uploading}>
                {uploading ? 'Connecting...' : 'Connect Insurance'}
              </button>
            {/if}
          </div>
        {:else if steps[currentStep].type === 'doctorData'}
          <div class="square-placeholder">
            {#if doctorDataUploaded}
              <div>Doctor Data Uploaded!</div>
            {:else}
              <label class="file-upload">
                <input type="file" on:change={handleDoctorDataUpload} disabled={uploading} />
                <span>{uploading ? 'Uploading...' : 'Upload Doctor Data'}</span>
              </label>
            {/if}
          </div>
        {:else if steps[currentStep].type === 'googleFit'}
          <div class="square-placeholder">
            {#if googleFitConnected}
              <div>Google Fit Connected!</div>
            {:else}
              <button class="action-btn" on:click={handleGoogleFitConnect} disabled={uploading}>
                {uploading ? 'Connecting...' : 'Connect Google Fit'}
              </button>
            {/if}
          </div>
        {:else if steps[currentStep].type === 'done'}
          <div class="square-placeholder">
            <div>🎉 All Done! Welcome aboard.</div>
          </div>
        {/if}
      </div>
      <div class="onboarding-actions">
        <button class="skip" on:click={handleSkip}>Skip</button>
        <button class="continue" on:click={handleContinue}>Continue</button>
      </div>
    </div>
  </div>
  
  <style>
    .onboarding-outer {
      min-height: 100vh;
      min-width: 100vw;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #f8fff9;
    }
    .onboarding-container {
      width: 90vw;
      max-width: 400px;
      height: 80vh;
      max-height: 700px;
      background: #fff;
      border-radius: 2rem;
      box-shadow: 0 4px 24px rgba(106,0,255,0.08);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      padding: 2rem 1.5rem;
      box-sizing: border-box;
      transition: box-shadow 0.2s;
    }
    .onboarding-title {
      font-family: 'DM Sans', sans-serif;
      font-size: 1.5rem;
      color: #6a00ff;
      margin-top: 1rem;
      text-align: center;
      font-weight: 600;
    }
    .onboarding-content {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100%;
    }
    .square-placeholder {
      width: min(60vw, 300px);
      height: min(60vw, 300px);
      background: #f8fff9;
      border: 2px dashed #6a00ff;
      border-radius: 1.5rem;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #6a00ff;
      font-size: 1.1rem;
      font-family: 'DM Sans', sans-serif;
      flex-direction: column;
      gap: 1rem;
    }
    .action-btn {
      background: #6a00ff;
      color: #fff;
      border: none;
      border-radius: 1rem;
      padding: 1rem 2rem;
      font-size: 1rem;
      font-family: 'DM Sans', sans-serif;
      cursor: pointer;
      transition: background 0.2s;
    }
    .action-btn:disabled {
      background: #ccc;
      cursor: not-allowed;
    }
    .file-upload {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 0.5rem;
      cursor: pointer;
      color: #6a00ff;
      font-family: 'DM Sans', sans-serif;
    }
    .file-upload input[type="file"] {
      display: none;
    }
    .file-upload span {
      background: #6a00ff;
      color: #fff;
      border-radius: 1rem;
      padding: 0.7rem 1.5rem;
      font-size: 1rem;
      cursor: pointer;
      transition: background 0.2s;
      display: inline-block;
    }
    .file-upload span:active {
      background: #7c1fff;
    }
    .onboarding-actions {
      display: flex;
      width: 100%;
      justify-content: space-between;
      margin-bottom: 1rem;
      gap: 1rem;
    }
    .onboarding-actions button {
      flex: 1;
      padding: 0.9rem 0;
      border-radius: 1rem;
      border: none;
      font-family: 'DM Sans', sans-serif;
      font-size: 1rem;
      font-weight: 500;
      cursor: pointer;
      transition: background 0.2s, color 0.2s;
    }
    .onboarding-actions .skip {
      background: #f8fff9;
      color: #6a00ff;
      border: 2px solid #6a00ff;
    }
    .onboarding-actions .skip:hover {
      background: #e7fff2;
    }
    .onboarding-actions .continue {
      background: #6a00ff;
      color: #fff;
      border: 2px solid #6a00ff;
    }
    .onboarding-actions .continue:hover {
      background: #7c1fff;
    }
  </style>