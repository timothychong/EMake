lock=`find . -name 'lock*' | wc -l`

# IF there is a lock then exit (It's currently run by someone else)
if [ "$lock" -gt 0 ]; then
    find . -name 'lock*'
    echo "Skipping Locked"
    exit
fi

done=`find . -name 'done' | wc -l`
if [ "$done" -gt 0 ]; then
    echo "Skipping Done"
    exit
fi

# Create lock
hostname=`hostname`
touch lock_$hostname

pwdd=`pwd`
echo "Running $pwdd"

# Execute command
source command.sh

# done
touch done

# remove lock
rm -f lock_$hostname
