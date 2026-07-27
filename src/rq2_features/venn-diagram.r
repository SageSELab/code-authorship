library(venn)
library(sets)
library(jsonlite)

# Read the file as a text string first
json_string <- readLines("./all_models_all_corrects.json", warn = FALSE)

# Join the lines in case it’s a multi-line JSON
#json_string <- paste(json_string, collapse = "")

# Now try to parse the JSON
df <- fromJSON(json_string)



codebert <- sample(df$CodeBERT)
contra_c <- sample(df$ContraBERT_C)
contra_g <- sample(df$ContraBERT_G)
graphcodebert <- sample(df$GraphCodeBERT)
unixcoder <- sample(df$UniXcoder)
#pbnn <- sample(df$PbNN)
deepseek <- sample(df$DeepSeek)
codellama <- sample(df$CodeLlama)

venn_list <- list(codellama, codebert, contra_c, contra_g, graphcodebert, unixcoder, deepseek)

pdf.options(family = "Times", pointsize = 12)

pdf("leetcode_dataset_orthogonality.pdf")



venn(venn_list, ilabels = FALSE, ilcs=.78,box = FALSE, snames = "CodeLlama, CodeBERT, ContraBERT_C, ContraBERT_G, GraphCodeBERT, UniXcoder, DeepSeek", show.plot = TRUE)


dev.off()

