# Create attributes file for input into PyMVPA

args <- commandArgs(trailingOnly=TRUE)
SUBID <- as.numeric(args[1])

file <- read.csv(paste0('../data/', SUBID, '/', SUBID, '_trialOnsets.txt', sep=""), 
                  sep = "\t", header = TRUE)
onset_times_sec <- file$TrialOnset/1000
onset_volumes <- round(onset_times_sec, digits=0)
onset_volumes2 <- onset_volumes+1 # each stimuli lasts for three volumes
onset_volumes3 <- onset_volumes+2
onset_volumes_all <- sort(c(onset_volumes, onset_volumes2, onset_volumes3))

categoriesmatrix <- stimulimatrix <- c()
for (i in 1:length(file$Category)){
  categoriesmatrix <- c(categoriesmatrix, rep(as.character(file$Category)[i],3))
  stimulimatrix <- c(stimulimatrix, rep(as.character(file$Stimulus)[i],3))
}

attributes_vol_cat <- cbind(as.data.frame(categoriesmatrix), onset_volumes_all)
attributes_vol_stim <- cbind(as.data.frame(stimulimatrix), onset_volumes_all)

num_vols <- 0:499
rest_vols <- num_vols[!num_vols %in% onset_volumes_all]
rest_target <- rep("rest", length(rest_vols))
rest_attributes <- cbind(as.data.frame(rest_target), as.data.frame(rest_vols))
names(attributes_vol_cat) <- names(attributes_vol_stim) <- names(rest_attributes) <- c("target", "chunk")
  
df_cat <- rbind(attributes_vol_cat, rest_attributes)
df_stim <- rbind(attributes_vol_stim, rest_attributes)
df_cat <- df_cat[order(df_cat$chunk),]
df_stim <- df_stim[order(df_stim$chunk),]
  
actualchunk <- rep(0,length(num_vols))
final_attributes_cat <- cbind(as.data.frame(df_cat$target), actualchunk)
final_attributes_stim <- cbind(as.data.frame(df_stim$target), actualchunk)

# create output dir, if necessary
outputDir <- file.path('../data', SUBID, '/timingFiles')
dir.create(outputDir, showWarnings = FALSE)
write.table(final_attributes_cat, file=file.path(outputDir, paste0(SUBID, '_attributes_category.txt')),
            row.names=FALSE, col.names=FALSE, quote=FALSE)
write.table(final_attributes_stim, file=file.path(outputDir, paste0(SUBID, '_attributes_stimuli.txt')),
            row.names=FALSE, col.names=FALSE, quote=FALSE)

