<script lang="ts">
    import GoogleFitForm from './GoogleFitForm.svelte';
    import NewInfoCheck from './NewInfoCheck.svelte';
    import VoiceChatStep from './VoiceChatStep.svelte';
    import { v4 as uuidv4 } from 'uuid';
    import { API_URL } from '../config';
    
    // Steps data model
    const steps = [
      { title: "Connect Your Insurance", type: "insurance" },
      { title: "Upload Latest Lab Report", type: "labReport" },
      { title: "Upload Latest Doctor's Letter", type: "doctorLetter" },
      { title: "Upload Latest Medical Information", type: "medicalInfo" },
      { title: "Connect Google Fit", type: "googleFit" },
      { title: "Voice Chat with AI Assistant", type: "voiceChat" },
      { title: "All Done!", type: "done" }
    ];
  
    let currentStep = 0;
    let showNewInfoCheck = true;
    let insuranceConnected = false;
    let labReportUploaded = false;
    let doctorLetterUploaded = false;
    let medicalInfoUploaded = false;
    let googleFitConnected = false;
    let voiceChatCompleted = false;
    let uploading = false;
    let labReportError = '';
    let doctorLetterError = '';
    let medicalInfoError = '';
    let labReportSuccess = '';
    let doctorLetterSuccess = '';
    let medicalInfoSuccess = '';
    let insuranceError = '';
    let insuranceSuccess = '';

    // Generate UUIDs for each upload type
    let insuranceUuid = uuidv4();
    let labReportUuid = uuidv4();
    let doctorLetterUuid = uuidv4();
    let medicalInfoUuid = uuidv4();

    function handleHasNewInfo() {
      showNewInfoCheck = false;
    }

    function handleNoNewInfo() {
      showNewInfoCheck = false;
      currentStep = steps.length - 1; // Set to the last step which is "All Done!"
    }

    // Reset UUIDs when moving to a new step
    function resetUuid(stepType: string) {
      switch(stepType) {
        case 'insurance':
          insuranceUuid = uuidv4();
          break;
        case 'labReport':
          labReportUuid = uuidv4();
          break;
        case 'doctorLetter':
          doctorLetterUuid = uuidv4();
          break;
        case 'medicalInfo':
          medicalInfoUuid = uuidv4();
          break;
      }
    }
  
    // Placeholder for backend logic
    async function handleInsuranceConnect() {
      // Simulate backend call
      insuranceConnected = false;
      uploading = true;
      await new Promise(r => setTimeout(r, 1000));
      insuranceConnected = true;
      uploading = false;
    }
  
    async function handleFileUpload(files: FileList, type: string) {
      uploading = true;
      // Reset all errors/success for the current type
      if (type === 'labData') {
        labReportError = '';
        labReportSuccess = '';
      } else if (type === 'doctorLetter') {
        doctorLetterError = '';
        doctorLetterSuccess = '';
      } else if (type === 'medicationPlan') {
        medicalInfoError = '';
        medicalInfoSuccess = '';
      }

      let uuid = '';
      if (type === 'labData') uuid = labReportUuid;
      else if (type === 'doctorLetter') uuid = doctorLetterUuid;
      else if (type === 'medicationPlan') uuid = medicalInfoUuid;

      try {
        // Upload all files first
        for (let i = 0; i < files.length; i++) {
          const formData = new FormData();
          formData.append('image', files[i]);

          const response = await fetch(`${API_URL}/upload-image?image_type=${type}&uuid=${uuid}`, {
            method: 'POST',
            body: formData,
            credentials: 'include'
          });
          const data = await response.json();
          
          if (!data.success) {
            throw new Error(data.message || 'Upload failed');
          }
        }

        // After all files are uploaded, trigger PDF conversion
        const pdfForm = new FormData();
        pdfForm.append('image_type', type);
        pdfForm.append('uuid', uuid);
        
        const pdfResponse = await fetch(`${API_URL}/convert-images-to-pdf`, {
          method: 'POST',
          body: pdfForm,
          credentials: 'include'
        });
        const pdfData = await pdfResponse.json();
        
        if (pdfData.success) {
          if (type === 'labData') {
            labReportUploaded = true;
            labReportSuccess = `${files.length} file(s) uploaded and processed successfully!`;
          } else if (type === 'doctorLetter') {
            doctorLetterUploaded = true;
            doctorLetterSuccess = `${files.length} file(s) uploaded and processed successfully!`;
          } else if (type === 'medicationPlan') {
            medicalInfoUploaded = true;
            medicalInfoSuccess = `${files.length} file(s) uploaded and processed successfully!`;
          }
          console.log('PDF generated:', pdfData.pdf_url);
        } else {
          throw new Error(pdfData.message || 'PDF generation failed');
        }
      } catch (error) {
        console.error('Upload error:', error);
        if (type === 'labData') {
          labReportError = 'Failed to process files. Please try again.';
        } else if (type === 'doctorLetter') {
          doctorLetterError = 'Failed to process files. Please try again.';
        } else if (type === 'medicationPlan') {
          medicalInfoError = 'Failed to process files. Please try again.';
        }
      } finally {
        uploading = false;
      }
    }

    async function handleInsuranceUpload(event: Event) {
      const target = event.target as HTMLInputElement;
      const files = target.files;
      if (files && files.length > 0) {
        uploading = true;
        insuranceError = '';
        insuranceSuccess = '';

        try {
          // Upload all files first
          for (let i = 0; i < files.length; i++) {
            const formData = new FormData();
            formData.append('image', files[i]);

            const response = await fetch(`${API_URL}/upload-image?image_type=insuranceCard&uuid=${insuranceUuid}`, {
              method: 'POST',
              body: formData,
              credentials: 'include'
            });
            const data = await response.json();
            
            if (!data.success) {
              throw new Error(data.message || 'Upload failed');
            }
          }
          
          // After all files are uploaded, trigger PDF conversion
          const pdfForm = new FormData();
          pdfForm.append('image_type', 'insuranceCard');
          pdfForm.append('uuid', insuranceUuid);
          
          const pdfResponse = await fetch(`${API_URL}/convert-images-to-pdf`, {
            method: 'POST',
            body: pdfForm,
            credentials: 'include'
          });
          const pdfData = await pdfResponse.json();
          
          if (pdfData.success) {
            insuranceConnected = true;
            insuranceSuccess = `${files.length} file(s) uploaded and processed successfully!`;
            console.log('Insurance PDF generated:', pdfData.pdf_url);
          } else {
            throw new Error(pdfData.message || 'PDF generation failed');
          }
        } catch (error) {
          console.error('Insurance upload error:', error);
          insuranceError = 'Failed to process files. Please try again.';
        } finally {
          uploading = false;
        }
      }
    }

    async function handleLabReportUpload(event: Event) {
      const target = event.target as HTMLInputElement;
      const files = target.files;
      if (files && files.length > 0) {
        await handleFileUpload(files, 'labData');
      }
    }

    async function handleDoctorLetterUpload(event: Event) {
      const target = event.target as HTMLInputElement;
      const files = target.files;
      if (files && files.length > 0) {
        await handleFileUpload(files, 'doctorLetter');
      }
    }

    async function handleMedicalInfoUpload(event: Event) {
      const target = event.target as HTMLInputElement;
      const files = target.files;
      if (files && files.length > 0) {
        await handleFileUpload(files, 'medicationPlan');
      }
    }

    function handleContinue() {
      if (currentStep < steps.length - 1) {
        // If next step is an upload step, generate a new UUID for it
        const nextType = steps[currentStep + 1].type;
        if (nextType === 'insurance') {
          insuranceUuid = uuidv4();
        } else if (nextType === 'labReport') {
          labReportUuid = uuidv4();
        } else if (nextType === 'doctorLetter') {
          doctorLetterUuid = uuidv4();
        } else if (nextType === 'medicalInfo') {
          medicalInfoUuid = uuidv4();
        }
        currentStep += 1;
      }
    }
  
    function handleSkip() {
      if (currentStep < steps.length - 1) {
        // If next step is an upload step, generate a new UUID for it
        const nextType = steps[currentStep + 1].type;
        if (nextType === 'insurance') {
          insuranceUuid = uuidv4();
        } else if (nextType === 'labReport') {
          labReportUuid = uuidv4();
        } else if (nextType === 'doctorLetter') {
          doctorLetterUuid = uuidv4();
        } else if (nextType === 'medicalInfo') {
          medicalInfoUuid = uuidv4();
        }
        currentStep += 1;
      }
    }
  
    // Optional: handle swipe/scroll navigation
    let startY = 0;
    function handleTouchStart(e: TouchEvent) {
      startY = e.touches[0].clientY;
    }
    function handleTouchEnd(e: TouchEvent) {
      const endY = e.changedTouches[0].clientY;
      if (startY - endY > 50) handleContinue(); // swipe up
      if (endY - startY > 50 && currentStep > 0) currentStep -= 1; // swipe down
    }

    function handleGoogleFitSkip() {
      handleSkip();
    }

    function handleGoogleFitContinue() {
      googleFitConnected = true;
      handleContinue();
    }

    function handleVoiceChatComplete() {
        voiceChatCompleted = true;
        currentStep++;
    }
</script>
  
<div
  class="onboarding-outer"
  on:touchstart={handleTouchStart}
  on:touchend={handleTouchEnd}
>
  {#if uploading}
    <div class="loading-overlay">
      <div class="loading-popup">
        <div class="loading-spinner"></div>
        <div class="loading-text">Uploading files...</div>
      </div>
    </div>
  {/if}

  {#if showNewInfoCheck}
    <NewInfoCheck on:hasNewInfo={handleHasNewInfo} on:noNewInfo={handleNoNewInfo} />
  {:else}
    <div class="onboarding-container">
      <div class="onboarding-title">{steps[currentStep].title}</div>
      <div class="onboarding-content">
        {#if steps[currentStep].type === 'insurance'}
          <div class="square-placeholder">
            {#if insuranceConnected}
              <div>Insurance Card Uploaded!</div>
            {:else}
              <label class="file-upload">
                <input type="file" accept="image/*" multiple on:change={handleInsuranceUpload} disabled={uploading} />
                <span>{uploading ? 'Uploading...' : 'Upload Insurance Card'}</span>
              </label>
              {#if insuranceError}
                <div class="error-message">{insuranceError}</div>
              {/if}
              {#if insuranceSuccess}
                <div class="success-message">{insuranceSuccess}</div>
              {/if}
            {/if}
          </div>
        {:else if steps[currentStep].type === 'labReport'}
          <div class="square-placeholder">
            {#if labReportUploaded}
              <div>Latest Lab Report Uploaded!</div>
            {:else}
              <label class="file-upload">
                <input type="file" accept="image/*" multiple on:change={handleLabReportUpload} disabled={uploading} />
                <span>{uploading ? 'Uploading...' : 'Upload Latest Lab Report'}</span>
              </label>
              {#if labReportError}
                <div class="error-message">{labReportError}</div>
              {/if}
              {#if labReportSuccess}
                <div class="success-message">{labReportSuccess}</div>
              {/if}
            {/if}
          </div>
        {:else if steps[currentStep].type === 'doctorLetter'}
          <div class="square-placeholder">
            {#if doctorLetterUploaded}
              <div>Latest Doctor's Letter Uploaded!</div>
            {:else}
              <label class="file-upload">
                <input type="file" accept="image/*" multiple on:change={handleDoctorLetterUpload} disabled={uploading} />
                <span>{uploading ? 'Uploading...' : 'Upload Latest Doctor\'s Letter'}</span>
              </label>
              {#if doctorLetterError}
                <div class="error-message">{doctorLetterError}</div>
              {/if}
              {#if doctorLetterSuccess}
                <div class="success-message">{doctorLetterSuccess}</div>
              {/if}
            {/if}
          </div>
        {:else if steps[currentStep].type === 'medicalInfo'}
          <div class="square-placeholder">
            {#if medicalInfoUploaded}
              <div>Latest Medical Information Uploaded!</div>
            {:else}
              <label class="file-upload">
                <input type="file" accept="image/*" multiple on:change={handleMedicalInfoUpload} disabled={uploading} />
                <span>{uploading ? 'Uploading...' : 'Upload Latest Medical Information'}</span>
              </label>
              {#if medicalInfoError}
                <div class="error-message">{medicalInfoError}</div>
              {/if}
              {#if medicalInfoSuccess}
                <div class="success-message">{medicalInfoSuccess}</div>
              {/if}
            {/if}
          </div>
        {:else if steps[currentStep].type === 'googleFit'}
          <GoogleFitForm 
            on:skip={handleGoogleFitSkip}
            on:continue={handleGoogleFitContinue}
          />
        {:else if steps[currentStep].type === 'voiceChat'}
          <VoiceChatStep on:complete={handleVoiceChatComplete} />
        {:else if steps[currentStep].type === 'done'}
          <div class="square-placeholder">
            <div>🎉 All Done! Welcome aboard.</div>
          </div>
        {/if}
      </div>
      {#if steps[currentStep].type !== 'googleFit' && steps[currentStep].type !== 'done'}
        <div class="onboarding-actions">
          <button class="skip" on:click={handleSkip}>Skip</button>
          <button class="continue" on:click={handleContinue}>Continue</button>
        </div>
      {/if}
    </div>
  {/if}
</div>
  
<style>
  .onboarding-outer {
    min-height: 100vh;
    min-width: 100vw;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f8fff9;
    padding: 1rem;
    box-sizing: border-box;
  }

  .onboarding-container {
    width: 100%;
    max-width: 400px;
    min-height: min(80vh, 600px);
    background: #fff;
    border-radius: 1.5rem;
    box-shadow: 0 4px 24px rgba(106,0,255,0.08);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 1.5rem;
    box-sizing: border-box;
    transition: box-shadow 0.2s;
    gap: 1.5rem;
  }

  .onboarding-title {
    font-family: 'DM Sans', sans-serif;
    font-size: clamp(1.25rem, 5vw, 1.5rem);
    color: #6a00ff;
    text-align: center;
    font-weight: 600;
    padding: 0 1rem;
    margin: 0;
  }

  .onboarding-content {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    flex: 1;
    min-height: min(60vh, 400px);
  }

  .square-placeholder {
    width: min(85vw, 300px);
    height: min(85vw, 300px);
    background: #f8fff9;
    border: 2px dashed #6a00ff;
    border-radius: 1.25rem;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #6a00ff;
    font-size: clamp(0.9rem, 4vw, 1.1rem);
    font-family: 'DM Sans', sans-serif;
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
    text-align: center;
  }

  .action-btn {
    background: #6a00ff;
    color: #fff;
    border: none;
    border-radius: 0.75rem;
    padding: 0.875rem 1.5rem;
    font-size: clamp(0.9rem, 4vw, 1rem);
    font-family: 'DM Sans', sans-serif;
    cursor: pointer;
    transition: background 0.2s;
    width: min(100%, 200px);
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
    width: 100%;
  }

  .file-upload input[type="file"] {
    display: none;
  }

  .file-upload span {
    background: #6a00ff;
    color: #fff;
    border-radius: 0.75rem;
    padding: 0.875rem 1.5rem;
    font-size: clamp(0.9rem, 4vw, 1rem);
    cursor: pointer;
    transition: background 0.2s;
    display: inline-block;
    text-align: center;
    width: min(100%, 200px);
  }

  .file-upload span:active {
    background: #7c1fff;
  }

  .onboarding-actions {
    display: flex;
    width: 100%;
    justify-content: space-between;
    gap: 0.75rem;
    margin: 0;
  }

  .onboarding-actions button {
    flex: 1;
    padding: 0.875rem 0;
    border-radius: 0.75rem;
    border: none;
    font-family: 'DM Sans', sans-serif;
    font-size: clamp(0.9rem, 4vw, 1rem);
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

  @media (max-width: 360px) {
    .onboarding-container {
      padding: 1rem;
      gap: 1rem;
    }

    .square-placeholder {
      padding: 0.75rem;
    }

    .onboarding-actions {
      gap: 0.5rem;
    }

    .onboarding-actions button {
      padding: 0.75rem 0;
    }
  }

  @media (max-height: 600px) {
    .onboarding-container {
      min-height: auto;
      padding: 1rem;
      gap: 1rem;
    }

    .onboarding-title {
      margin: 0;
    }

    .onboarding-content {
      min-height: min(50vh, 300px);
    }

    .square-placeholder {
      height: min(70vw, 250px);
    }
  }

  .error-message {
    color: #dc2626;
    font-size: 0.875rem;
    margin-top: 0.5rem;
    text-align: center;
  }

  .success-message {
    color: #059669;
    font-size: 0.875rem;
    margin-top: 0.5rem;
    text-align: center;
  }

  .loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }

  .loading-popup {
    background: white;
    padding: 2rem;
    border-radius: 1rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.1);
  }

  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #6a00ff;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  .loading-text {
    color: #6a00ff;
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
</style>