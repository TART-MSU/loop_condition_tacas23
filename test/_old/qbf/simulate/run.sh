#!/bin/sh

# HyperQube
GENQBF=../HyperQube/genqbf
QUABS=../HyperQube/quabs

GEN_M1=gen_model_a.java 	# K1
GEN_M2=gen_model_b.java		# K2
GEN_M3=gen_model_b.java		# K3

QS=AE	# quantifier selections
k=2		# bound of traces	
	
# models
I=model_a_I.bool
R=model_a_R.bool
J=model_b_I.bool
S=model_b_R.bool

# no use
Q=model_a_I.bool
W=model_a_I.bool
Z=model_a_I.bool
X=model_a_I.bool
C=model_a_I.bool
V=model_a_I.bool

# property
P=test_P.bool

# output files
QCIR_OUT=out.qcir
QUABS_OUT=out.quabs

# simple mapping of variable names and values
MAP=util/simple_map.java
MAP_OUT1=mapping_byName.cex
MAP_OUT2=mapping_byTime.cex

# simple parsing of booleans to digits
# PARSE=util/example_parser.java
# PARSE_OUT=parsed_mapping.cex

# for extracting one good mapping
PARSE=util/example_parser.java
PARSE_OUT=a_good_mapping.cex


# for extracting all good mappings
PARSE=util/goodmapping_parser.java
PARSE_OUT=all_good_mappings.cex


# for extracting bad mappings
# PARSE=util/badmapping_parser.java
# PARSE_OUT=all_bad_mappings.cex


make clean

# have a clean file
>${PARSE_OUT}
echo "Mapping Synthesis!">${PARSE_OUT}

java ${GEN_M2} #k2 and k3 will stay the same, 
java ${GEN_M3} 


>${MAP_OUT1} # clean up
>${MAP_OUT2} # clean up
# MAPPING_SELECTION=${i}

echo "---(START)---"
echo "mapping selection: " ${i}
echo "QS:" ${QS} "k=" ${k}  
# echo "---Generating boolean expressions---"
echo "constructing K1, K2, K3..."
java ${GEN_M1} 

# echo "---Generating QCIR---"
echo "generating QBF BMC..."
${GENQBF} -I ${I} -R ${R} -J ${J} -S ${S} -Q ${Q} -W ${W} -Z ${Z} -X ${X} -C ${C} -V ${V} -P ${P} -k ${k} -F ${QS}  -f qcir -o ${QCIR_OUT} -sem PES -n

# echo "---QUABS solving---"
echo "solving QBF..."
${QUABS}  --partial-assignment ${QCIR_OUT} 2>&1 | tee ${QUABS_OUT}
# time ${QUABS} --statistics --preprocessing 0 --partial-assignment ${QCIR_OUT} 2>&1 | tee ${QUABS_OUT}


echo "parsing into readable format..."
# echo "---Counterexample Mapping---"
java ${MAP} ${QCIR_OUT} ${QUABS_OUT} ${MAP_OUT1} ${MAP_OUT2}

# echo "---Parse All Binary Numbers---"
java ${PARSE} ${MAP_OUT2} ${PARSE_OUT} ${i}	 #by time

echo "---(END)---\n"


