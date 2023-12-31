library(shiny)
library(DT)
library(RColorBrewer)

# Define any Python packages needed for the app here:
PYTHON_DEPENDENCIES = c('pip', 'numpy')

# Begin app server
shinyServer(function(input, output) {
  
  # ------------------ App virtualenv setup (Do not edit) ------------------- #
  
  virtualenv_dir = Sys.getenv('VIRTUALENV_NAME')
  python_path = Sys.getenv('PYTHON_PATH')
  reticulate::install_python(version = "3.9:latest", list = FALSE, force = FALSE)
  # Create virtual env and install dependencies
  reticulate::virtualenv_create(envname = virtualenv_dir, python = python_path)
  reticulate::virtualenv_install(virtualenv_dir, packages = PYTHON_DEPENDENCIES, ignore_installed=TRUE)
  reticulate::use_virtualenv(virtualenv_dir, required = T)
  
  # ------------------ App server logic (Edit anything below) --------------- #
  
  plot_cols <- brewer.pal(11, 'Spectral')
  
  # Import python functions to R
  reticulate::source_python('python_functions.py')
  
  # Generate the requested distribution
  d <- reactive({
    dist <- switch(input$dist,
                   norm = rnorm,
                   unif = runif,
                   lnorm = rlnorm,
                   exp = rexp,
                   rnorm)
    
    return(dist(input$n))
  })
  
  # Generate a plot of the data
  output$plot <- renderPlot({
    dist <- input$dist
    n <- input$n
    
    return(hist(d(),
                main = paste0('Distribution plot: ', dist, '(n = ', n, ')'),
                xlab = '',
                col = plot_cols))
  })
  
  # Test that the Python functions have been imported
  output$message <- renderText({
    return(test_string_function(input$str))
  })
  
  # Test that numpy function can be used
  output$xy <- renderText({
    z = test_numpy_function(input$x, input$y)
    return(paste0('x + y = ', z))
  })
  
  # Display info about the system running the code
  output$sysinfo <- DT::renderDataTable({
    s = Sys.info()
    df = data.frame(Info_Field = names(s),
                    Current_System_Setting = as.character(s))
    return(datatable(df, rownames = F, selection = 'none',
                     style = 'bootstrap', filter = 'none', options = list(dom = 't')))
  })
  
  # Display system path to python
  output$which_python <- renderText({
    paste0('which python: ', Sys.which('python'))
  })
  
  # Display Python version
  output$python_version <- renderText({
    rr = reticulate::py_discover_config(use_environment = 'python35_env')
    paste0('Python version: ', rr$version)
  })
  
  # Display RETICULATE_PYTHON
  output$ret_env_var <- renderText({
    paste0('RETICULATE_PYTHON: ', Sys.getenv('RETICULATE_PYTHON'))
  })
  
  # Display virtualenv root
  output$venv_root <- renderText({
    paste0('virtualenv root: ', reticulate::virtualenv_root())
  })
  
})

# #
# # This is the server logic of a Shiny web application. You can run the
# # application by clicking 'Run App' above.
# #
# # Find out more about building applications with Shiny here:
# #
# #    http://shiny.rstudio.com/
# #
# 
# library(shiny)
# 
# # Define server logic required to draw a histogram
# function(input, output, session) {
# 
#     output$distPlot <- renderPlot({
# 
#         # generate bins based on input$bins from ui.R
#         x    <- faithful[, 2]
#         bins <- seq(min(x), max(x), length.out = input$bins + 1)
# 
#         # draw the histogram with the specified number of bins
#         hist(x, breaks = bins, col = 'darkgray', border = 'white',
#              xlab = 'Waiting time to next eruption (in mins)',
#              main = 'Histogram of waiting times')
# 
#     })
# 
# }






##################
# library(shiny)
# library(reticulate)  # Load the reticulate package
# 
# # Define server logic required to draw a histogram
# function(input, output, session) {
#   
#   # Define a function to run the Python code and return the output
#   run_python_code <- function() {
#     use_python("path_to_your_python_binary")  # Set the path to your Python binary
#     
#     # Load the Python code
#     source_python("path_to_your_python_script.py")  # Set the path to your Python script
# 
#     # Call the Python function
#     classifier_path <- '../saved_classifiers/bury_pnas_21/len500/best_model_1_1_len500.pkl'
#     classifier <- load_model(classifier_path)
#     result <- ts_may.apply_classifier(classifier, tmin=0, tmax=400)
#     
#     # Release the Python environment
#     py_run_string("py <- NULL")
#     
#     return(result)
#   }
#   
#   output$distPlot <- renderPlot({
#     # Call the Python function and get the result
#     python_result <- run_python_code()
#     
#     # Generate bins based on the Python output (assuming it's a vector)
#     bins <- seq(min(python_result), max(python_result), length.out = input$bins + 1)
#     
#     # Draw the histogram with the specified number of bins
#     hist(python_result, breaks = bins, col = 'darkgray', border = 'white',
#          xlab = 'Waiting time to next eruption (in mins)',
#          main = 'Histogram of waiting times')
#   })
# }

