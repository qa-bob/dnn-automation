pipeline {
    agent any
    
    parameters {
        choice(
            name: 'BROWSER',
            choices: ['chrome', 'firefox'],
            description: 'Browser to run tests'
        )
        choice(
            name: 'TEST_SUITE',
            choices: ['smoke', 'regression', 'functional', 'authentication', 'dynamic_content', 'user_interactions', 'performance', 'all'],
            description: 'Test suite to run'
        )
        choice(
            name: 'ENVIRONMENT',
            choices: ['dev', 'staging', 'prod'],
            description: 'Environment to test against'
        )
        booleanParam(
            name: 'HEADLESS',
            defaultValue: true,
            description: 'Run tests in headless mode'
        )
        booleanParam(
            name: 'PARALLEL',
            defaultValue: false,
            description: 'Run tests in parallel'
        )
        string(
            name: 'WORKERS',
            defaultValue: '4',
            description: 'Number of parallel workers (if parallel is enabled)'
        )
        booleanParam(
            name: 'DOCKER_RUN',
            defaultValue: false,
            description: 'Run tests in Docker container'
        )
    }
    
    environment {
        PYTHON_VERSION = '3.11'
        REPORT_DIR = 'reports'
        SCREENSHOT_DIR = 'screenshots'
        VENV_DIR = 'venv'
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "🚀 Starting Test Automation Pipeline"
                    echo "Browser: ${params.BROWSER}"
                    echo "Test Suite: ${params.TEST_SUITE}"
                    echo "Environment: ${params.ENVIRONMENT}"
                    echo "Headless: ${params.HEADLESS}"
                    echo "Parallel: ${params.PARALLEL}"
                    echo "Docker: ${params.DOCKER_RUN}"
                }
                
                checkout scm
                
                // Clean workspace
                sh '''
                    rm -rf reports screenshots downloads venv
                    mkdir -p reports screenshots downloads
                '''
            }
        }
        
        stage('Setup Environment') {
            when {
                not { params.DOCKER_RUN }
            }
            steps {
                script {
                    echo "🔧 Setting up Python environment"
                }
                
                sh '''
                    python${PYTHON_VERSION} -m venv ${VENV_DIR}
                    source ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Docker Setup') {
            when {
                params.DOCKER_RUN
            }
            steps {
                script {
                    echo "🐳 Setting up Docker environment"
                }
                
                dir('test_automation_framework') {
                    sh '''
                        docker-compose -f docker/docker-compose.yml build test
                    '''
                }
            }
        }
        
        stage('Lint and Code Quality') {
            when {
                not { params.DOCKER_RUN }
            }
            steps {
                script {
                    echo "🔍 Running code quality checks"
                }
                
                sh '''
                    source ${VENV_DIR}/bin/activate
                    # Install linting tools
                    pip install flake8 pylint black isort
                    
                    # Run linting (continue on error for now)
                    flake8 pages/ utils/ config/ tests/ --max-line-length=120 --ignore=E203,W503 || true
                    
                    # Check import sorting
                    isort --check-only pages/ utils/ config/ tests/ || true
                    
                    # Check code formatting
                    black --check pages/ utils/ config/ tests/ || true
                '''
            }
        }
        
        stage('Run Tests') {
            parallel {
                stage('Standard Execution') {
                    when {
                        not { params.DOCKER_RUN }
                    }
                    steps {
                        script {
                            echo "🧪 Running tests with standard execution"
                            
                            def testCommand = "source ${VENV_DIR}/bin/activate && python run_tests.py"
                            testCommand += " --browser ${params.BROWSER}"
                            testCommand += " --env ${params.ENVIRONMENT}"
                            testCommand += " --html-report"
                            testCommand += " --verbose"
                            
                            if (params.HEADLESS) {
                                testCommand += " --headless"
                            } else {
                                testCommand += " --no-headless"
                            }
                            
                            if (params.PARALLEL) {
                                testCommand += " --parallel --workers ${params.WORKERS}"
                            }
                            
                            if (params.TEST_SUITE != 'all') {
                                if (params.TEST_SUITE in ['smoke', 'regression', 'functional', 'performance']) {
                                    testCommand += " --${params.TEST_SUITE}"
                                } else {
                                    testCommand += " -m ${params.TEST_SUITE}"
                                }
                            }
                            
                            echo "Executing: ${testCommand}"
                        }
                        
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            sh '''
                                source ${VENV_DIR}/bin/activate
                                cd test_automation_framework
                                python run_tests.py \
                                    --browser ${BROWSER} \
                                    --env ${ENVIRONMENT} \
                                    --html-report \
                                    --verbose \
                                    ${HEADLESS == 'true' ? '--headless' : '--no-headless'} \
                                    ${PARALLEL == 'true' ? "--parallel --workers ${WORKERS}" : ''} \
                                    ${TEST_SUITE != 'all' ? (TEST_SUITE in ['smoke', 'regression', 'functional', 'performance'] ? "--${TEST_SUITE}" : "-m ${TEST_SUITE}") : ''}
                            '''
                        }
                    }
                }
                
                stage('Docker Execution') {
                    when {
                        params.DOCKER_RUN
                    }
                    steps {
                        script {
                            echo "🐳 Running tests with Docker"
                            
                            def dockerService = 'test'
                            if (params.TEST_SUITE == 'smoke') {
                                dockerService = 'test-smoke'
                            } else if (params.TEST_SUITE == 'regression') {
                                dockerService = 'test-regression'
                            } else if (params.TEST_SUITE == 'performance') {
                                dockerService = 'test-performance'
                            } else if (params.BROWSER == 'firefox') {
                                dockerService = 'test-firefox'
                            }
                            
                            echo "Using Docker service: ${dockerService}"
                        }
                        
                        dir('test_automation_framework') {
                            catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                                sh '''
                                    export TEST_ENV=${ENVIRONMENT}
                                    export BROWSER=${BROWSER}
                                    export HEADLESS=${HEADLESS}
                                    
                                    docker-compose -f docker/docker-compose.yml up --abort-on-container-exit ${dockerService}
                                '''
                            }
                        }
                    }
                }
            }
        }
        
        stage('Collect Results') {
            steps {
                script {
                    echo "📊 Collecting test results"
                }
                
                // Copy results from Docker if needed
                script {
                    if (params.DOCKER_RUN) {
                        dir('test_automation_framework') {
                            sh '''
                                # Copy results from Docker container
                                docker-compose -f docker/docker-compose.yml cp test:/usr/src/app/reports ./reports || true
                                docker-compose -f docker/docker-compose.yml cp test:/usr/src/app/screenshots ./screenshots || true
                                
                                # Move to parent directory
                                cp -r reports ../reports || true
                                cp -r screenshots ../screenshots || true
                            '''
                        }
                    } else {
                        sh '''
                            # Copy results from test_automation_framework directory
                            cp -r test_automation_framework/reports/* reports/ || true
                            cp -r test_automation_framework/screenshots/* screenshots/ || true
                        '''
                    }
                }
            }
        }
        
        stage('Archive Results') {
            steps {
                script {
                    echo "📁 Archiving test results"
                }
                
                // Archive screenshots
                archiveArtifacts artifacts: 'screenshots/**/*.png', 
                                allowEmptyArchive: true, 
                                fingerprint: true
                
                // Archive reports
                archiveArtifacts artifacts: 'reports/**/*', 
                                allowEmptyArchive: true, 
                                fingerprint: true
                
                // Publish HTML report
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'test_report.html',
                    reportName: 'Test Automation Report',
                    reportTitles: 'Test Results'
                ])
            }
        }
        
        stage('Test Analytics') {
            steps {
                script {
                    echo "📈 Generating test analytics"
                }
                
                // Generate test summary
                sh '''
                    echo "Test Execution Summary" > test_summary.txt
                    echo "======================" >> test_summary.txt
                    echo "Browser: ${BROWSER}" >> test_summary.txt
                    echo "Test Suite: ${TEST_SUITE}" >> test_summary.txt
                    echo "Environment: ${ENVIRONMENT}" >> test_summary.txt
                    echo "Execution Mode: ${DOCKER_RUN == 'true' ? 'Docker' : 'Standard'}" >> test_summary.txt
                    echo "Timestamp: $(date)" >> test_summary.txt
                    echo "" >> test_summary.txt
                    
                    # Count test results if HTML report exists
                    if [ -f "reports/test_report.html" ]; then
                        echo "HTML Report Generated: Yes" >> test_summary.txt
                    else
                        echo "HTML Report Generated: No" >> test_summary.txt
                    fi
                    
                    # Count screenshots
                    screenshot_count=$(find screenshots -name "*.png" 2>/dev/null | wc -l)
                    echo "Screenshots Captured: $screenshot_count" >> test_summary.txt
                '''
                
                // Archive summary
                archiveArtifacts artifacts: 'test_summary.txt', 
                                allowEmptyArchive: true
            }
        }
    }
    
    post {
        always {
            script {
                echo "🧹 Cleaning up"
            }
            
            // Clean up Docker containers
            sh '''
                if [ "${DOCKER_RUN}" = "true" ]; then
                    cd test_automation_framework
                    docker-compose -f docker/docker-compose.yml down --volumes --remove-orphans || true
                fi
            '''
            
            // Clean up virtual environment
            sh '''
                rm -rf ${VENV_DIR} || true
            '''
        }
        
        success {
            script {
                echo "✅ Pipeline completed successfully!"
                
                // Send success notification
                if (env.SLACK_WEBHOOK_URL) {
                    slackSend(
                        channel: '#test-automation',
                        color: 'good',
                        message: "✅ Test Automation Pipeline Succeeded\n" +
                                "Job: ${env.JOB_NAME}\n" +
                                "Build: ${env.BUILD_NUMBER}\n" +
                                "Browser: ${params.BROWSER}\n" +
                                "Test Suite: ${params.TEST_SUITE}\n" +
                                "Environment: ${params.ENVIRONMENT}"
                    )
                }
            }
        }
        
        failure {
            script {
                echo "❌ Pipeline failed!"
                
                // Send failure notification
                if (env.SLACK_WEBHOOK_URL) {
                    slackSend(
                        channel: '#test-automation',
                        color: 'danger',
                        message: "❌ Test Automation Pipeline Failed\n" +
                                "Job: ${env.JOB_NAME}\n" +
                                "Build: ${env.BUILD_NUMBER}\n" +
                                "Browser: ${params.BROWSER}\n" +
                                "Test Suite: ${params.TEST_SUITE}\n" +
                                "Environment: ${params.ENVIRONMENT}\n" +
                                "Build URL: ${env.BUILD_URL}"
                    )
                }
            }
        }
        
        unstable {
            script {
                echo "⚠️ Pipeline completed with test failures!"
                
                // Send unstable notification
                if (env.SLACK_WEBHOOK_URL) {
                    slackSend(
                        channel: '#test-automation',
                        color: 'warning',
                        message: "⚠️ Test Automation Pipeline Unstable\n" +
                                "Job: ${env.JOB_NAME}\n" +
                                "Build: ${env.BUILD_NUMBER}\n" +
                                "Browser: ${params.BROWSER}\n" +
                                "Test Suite: ${params.TEST_SUITE}\n" +
                                "Environment: ${params.ENVIRONMENT}\n" +
                                "Some tests failed - check report for details"
                    )
                }
            }
        }
    }
}
