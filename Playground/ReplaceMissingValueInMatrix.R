{
  library(dplyr)
  # Missing value is NA
  mtx <- matrix(c(1, NA, 3, NA, NA, NA, 7, NA, 9), nrow = 3, ncol = 3)
  print(mtx)
  
  # Convert to a data frame
  mtx <- as.data.frame(mtx)
  
  # Convert to a list by row names
  mtx <- split(mtx, rownames(mtx))
  
  #' Fill NA With Average Function
  #' @input x is a data frame with 1 x N dimension
  #' 
  fillNAWithAverage <- function (x) {
    # Check if any NA exist
    # If the entire row are NA, fill with 0
    if (sum(is.na(x)) == ncol(x)) {
      x[is.na(x)] <- 0
    } else if (sum(is.na(x)) > 0) {
      
      # Loop through all columns
      for (i in 1:ncol(x)) {
        
        # if any value is NA, fill with the average of that row 
        if (is.na(x[1, i])) {
          # Set na.rm = TRUE to ignore NAs
          x[1, i] <- rowMeans(x, na.rm = TRUE)
        }
      }
    }
    # Return x
    return(x)
  }
  
  # Use lapply to apply the function to all member of the list
  output <- lapply(mtx, fillNAWithAverage)
  
  # Convert list back to data frame
  output <- dplyr::bind_rows(output)
  print(output)
}

