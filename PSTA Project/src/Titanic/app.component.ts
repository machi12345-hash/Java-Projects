import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatTabsModule } from '@angular/material/tabs';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatExpansionModule } from '@angular/material/expansion';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatToolbarModule,
    MatButtonModule, 
    MatCardModule,
    MatInputModule,
    MatSelectModule,
    MatCheckboxModule,
    MatTabsModule,
    MatProgressSpinnerModule,
    MatExpansionModule
  ],
  template: `
    <div class="app-container">
      <header class="app-header">
        <h1>COBOL Dependency Analyzer</h1>
      </header>

      <main class="app-content">
        <mat-tabs>
          <mat-tab label="Job Dependencies">
            <div class="tab-content">
              <mat-card class="prompt-card">
                <mat-card-content>
                  <mat-form-field appearance="outline" class="full-width">
                    <mat-label>Enter your prompt</mat-label>
                    <textarea matInput 
                      [(ngModel)]="prompt" 
                      placeholder="Example: Give me the dependencies for BF4000M1"
                      rows="3"></textarea>
                  </mat-form-field>
                  
                  <div class="actions">
                    <mat-form-field appearance="outline">
                      <mat-label>Select type</mat-label>
                      <mat-select [(ngModel)]="selectedType">
                        <mat-option *ngFor="let type of dependencyTypes" [value]="type">
                          {{type}}
                        </mat-option>
                      </mat-select>
                    </mat-form-field>
                    
                    <button mat-raised-button color="primary" (click)="analyze()">
                      Analyze
                    </button>
                  </div>
                </mat-card-content>
              </mat-card>
              
              <div *ngIf="loading" class="loading-container">
                <mat-spinner diameter="40"></mat-spinner>
                <p>Analyzing dependencies...</p>
              </div>
              
              <div *ngIf="showGraph" class="graph-container">
                <div class="filter-options">
                  <mat-checkbox [(ngModel)]="filters.applications" (change)="updateFilters()">
                    Show Applications
                  </mat-checkbox>
                  <mat-checkbox [(ngModel)]="filters.jobs" (change)="updateFilters()">
                    Show Jobs
                  </mat-checkbox>
                  <mat-checkbox [(ngModel)]="filters.programs" (change)="updateFilters()">
                    Show Programs
                  </mat-checkbox>
                  <mat-checkbox [(ngModel)]="filters.subPrograms" (change)="updateFilters()">
                    Show Sub-Programs
                  </mat-checkbox>
                </div>
                
                <div class="graph">
                  <!-- Graph placeholder -->
                  <div class="graph-placeholder">
                    <div class="node application">Application</div>
                    <div class="connection"></div>
                    <div class="node job">Job 1</div>
                    <div class="connection"></div>
                    <div class="node program">Program 1</div>
                    <div class="connection"></div>
                    <div class="node subprogram">Sub-Program 1</div>
                  </div>
                </div>
              </div>
            </div>
          </mat-tab>
          
          <mat-tab label="Create Documentation">
            <div class="tab-content">
              <mat-card class="prompt-card">
                <mat-card-content>
                  <mat-form-field appearance="outline" class="full-width">
                    <mat-label>Enter program name</mat-label>
                    <textarea matInput 
                      [(ngModel)]="docPrompt" 
                      placeholder="Example: Generate documentation for P4000M1"
                      rows="3"></textarea>
                  </mat-form-field>
                  
                  <div class="actions">
                    <button mat-raised-button color="primary" (click)="generateDoc()">
                      Generate Documentation
                    </button>
                  </div>
                </mat-card-content>
              </mat-card>
              
              <div *ngIf="docLoading" class="loading-container">
                <mat-spinner diameter="40"></mat-spinner>
                <p>Generating documentation... This may take a few minutes.</p>
              </div>
              
              <div *ngIf="showDocumentation" class="documentation-container">
                <div class="doc-actions">
                  <button mat-raised-button color="primary">
                    Download PDF
                  </button>
                </div>
                
                <mat-expansion-panel>
                  <mat-expansion-panel-header>
                    <mat-panel-title>
                      Documentation Preview
                    </mat-panel-title>
                  </mat-expansion-panel-header>
                  
                  <div class="doc-content">
                    <h1>BF4000M1</h1>
                    <h2>Report date: 2025-04-02T10:15:30.123Z</h2>
                    
                    <h2>Table of Contents</h2>
                    <p>1. Program Overview</p>
                    <p>2. Program Architecture</p>
                    <p>3. Program Structure</p>
                    <p>4. Data Management</p>
                    <p>5. Control Flow</p>
                    <p>6. Error Handling</p>
                    <p>7. Integration & Interfaces</p>
                    
                    <h2>1. Program Overview</h2>
                    <p>This is a sample program documentation that would be generated from the actual code analysis. The program appears to be responsible for processing financial transactions related to customer accounts...</p>
                    
                    <h2>2. Program Architecture</h2>
                    <p>The program is structured as a batch processing application that interfaces with multiple external systems including the customer database, transaction log, and reporting systems...</p>
                  </div>
                </mat-expansion-panel>
              </div>
            </div>
          </mat-tab>
        </mat-tabs>
      </main>
    </div>
  `,
  styles: [`
    .app-container {
      display: flex;
      flex-direction: column;
      min-height: 100vh;
      background-image: url('/assets/cda.png');
      background-size: cover;
      background-position: center;
      background-attachment: fixed;
    }

    .app-header {
      padding: 20px;
      text-align: center;
    }

    .app-header h1 {
      color: white;
      margin: 0;
      font-size: 32px;
      text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.7);
    }

    .app-content {
      flex: 1;
      padding: 20px;
      max-width: 1200px;
      margin: 0 auto;
      width: 100%;
    }

    ::ng-deep .mat-mdc-tab-body-wrapper {
      background-color: rgba(255, 255, 255, 0.9);
      border-radius: 8px;
      padding: 20px;
      margin-top: 10px;
    }

    .tab-content {
      padding: 10px;
    }

    .prompt-card {
      margin-bottom: 20px;
    }

    .full-width {
      width: 100%;
    }

    .actions {
      display: flex;
      gap: 15px;
      align-items: center;
      margin-top: 15px;
    }

    .loading-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin: 30px 0;
    }

    .graph-container, .documentation-container {
      margin-top: 20px;
      padding: 15px;
      background-color: white;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .filter-options {
      display: flex;
      gap: 20px;
      flex-wrap: wrap;
      margin-bottom: 15px;
      padding: 10px;
      background-color: #f5f5f5;
      border-radius: 4px;
    }

    .graph {
      height: 500px;
      border: 1px solid #ddd;
      border-radius: 4px;
      position: relative;
      background-color: white;
    }

    .graph-placeholder {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100%;
      gap: 20px;
    }

    .node {
      padding: 10px 20px;
      border-radius: 20px;
      color: white;
      text-align: center;
      width: 120px;
    }

    .application {
      background-color: grey;
    }

    .job {
      background-color: lime;
      color: black;
    }

    .program {
      background-color: aqua;
      color: black;
    }

    .subprogram {
      background-color: orange;
      color: black;
    }

    .connection {
      height: 20px;
      width: 2px;
      background-color: #333;
    }

    .doc-actions {
      margin-bottom: 15px;
    }

    .doc-content {
      max-height: 400px;
      overflow-y: auto;
      padding: 15px;
      background-color: #f9f9f9;
      border-radius: 4px;
      font-family: 'Arial', sans-serif;
    }

    .doc-content h1 {
      font-size: 24px;
      color: #333;
      margin-top: 0;
    }

    .doc-content h2 {
      font-size: 20px;
      color: #444;
      margin-top: 20px;
      border-bottom: 1px solid #ddd;
      padding-bottom: 5px;
    }

    ::ng-deep .mat-mdc-tab-header {
      background-color: rgba(255, 255, 255, 0.9);
      border-radius: 8px 8px 0 0;
    }
  `]
})
export class AppComponent {
  prompt: string = '';
  docPrompt: string = '';
  dependencyTypes: string[] = ['Job dependencies', 'Create documentation'];
  selectedType: string = 'Job dependencies';
  
  loading: boolean = false;
  docLoading: boolean = false;
  showGraph: boolean = false;
  showDocumentation: boolean = false;
  
  filters = {
    applications: true,
    jobs: true,
    programs: true,
    subPrograms: true
  };
  
  analyze() {
    this.loading = true;
    
    // Simulate API call
    setTimeout(() => {
      this.loading = false;
      this.showGraph = true;
    }, 2000);
  }
  
  generateDoc() {
    this.docLoading = true;
    
    // Simulate API call
    setTimeout(() => {
      this.docLoading = false;
      this.showDocumentation = true;
    }, 3000);
  }
  
  updateFilters() {
    // In a real app, this would update the graph visualization
    console.log('Filters updated:', this.filters);
  }
}