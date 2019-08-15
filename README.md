# MiniFlow : Mini Bioinformatics expressive Pipelines Engine

## Introduction

Miniflow is a simple yet powerful bioinformatics workflow/pipeline engine that you can express your overall bioinformatics pipeline in pure python code.

It gives you much more power and control over your pipeline and also gives you completely independent and easy way to express interdependencies between tasks in a workflow.

## how to install 

Install all dependencies in requirements.txt file associated with this project

``
pip install -r requirements.txt
``

## How to use 

Simple RNA-seq Data analysis pipeline , this pipeline simply 

1 - Perform Quality report generation
2 - Perform Quality Control by trimming and filtering
3 - Aligning the trimmed fastq against the indexed reference genome of homo sapiens and finally notify the user via email that the alignment 
task has been finished




```


from miniflow import *

p = Project(base_dir="/home/snouto/bioinf/miniflow",data_dir="/home/snouto/bioinf/data")

p.then(Task("QC","fastqc {{data_dir}}/SRR8436151.fastq")

.then(Task("QCC","java -jar trimmomatic.jar","SE -phred33","{{data_dir}}/SRR8436151.fastq","{{QCC_dir}}/SR8436151.trimmed.fastq","LEADING:20","TRAILING:20","MINLEN:50"))


.then(Task("Alignment","tophat --GTF {{data_dir}}/igenomes/hs/genes.gtf","--library-type=fr-unstranded","--num-threads 4" ,"-o {{Alignment_dir}}","{{data_dir}}/index/hs","{{QCC_dir}}/SR8436151.trimmed.fastq",notify=True))

.run()

```

