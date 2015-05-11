# svn copy trunk/ tags/TAG_NAME

# List modules used (inserted into "py_modules" section of setup.py)
echo -e	"\t            'Puzzlebox.Jigsaw', \\"

for each in `ls Puzzlebox/Jigsaw/*.py | grep -v __ | grep -v Puzzlebox/Jigsaw/Slideshow | sort`
	do echo -e "\t            '$each', \\" | \
		sed s/\\//\\./ | \
		sed s/\\//\\./ | \
		sed s/.py//
done

echo -e "\t            'Puzzlebox.Jigsaw.Modules', \\"

for each in `ls Puzzlebox/Jigsaw/Modules/* | grep -v __ | grep -v .py | sort`
	do echo -e "\t            '$each', \\" | \
		sed s/\\//\\./ | \
		sed s/\\//\\./ | \
		sed s/\\//\\./ | \
		sed s/\\//\\./ | \
		sed s/://
done

for each in `ls Puzzlebox/Jigsaw/Modules/*/*.py | grep -v __ | sort`
	do echo -e "\t            '$each', \\" | \
		sed s/\\//\\./ | \
		sed s/\\//\\./ | \
		sed s/\\//\\./ | \
		sed s/\\//\\./ | \
		sed s/.py//
done

for each in `ls Puzzlebox/Synapse/*.py | grep -v __ | sort`
        do echo -e "\t            '$each', \\" | \
                sed s/\\//\\./ | \
                sed s/\\//\\./ | \
                sed s/.py//
done

python setup.py bdist_rpm
