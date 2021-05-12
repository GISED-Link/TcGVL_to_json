# TcGVL_to_json
Create a json writer and reader for a given TcGVL file

The writer is the part of the program that allows you to save a Twincat structure into a string in json format.
The reader is the part that set the structure from a json string.

## how to use it

1. To make things running, create a global variable file in the Twincat IDE. Create some variables. Then add {attribute 'to_json'} above the variables you need to save and restore.
2. Open this program. Inform the TcGVL file and the project directory
3. Run it
4. You will see the result in the 4 text windows.
5. The 2 left windows are the writer, the right ones are the reader. The top is the local variables declaration, the bottom part is the code

hope you enjoy it

## known limitation
* boolean type is not supported, yet (easy to do)
* Time, date, wstring are not supported
* Nested names that are the same is not (well) supported. See explanation below


About nested names:

    station2
        axis1
            position
            velocity
        axis2
            position        // this is ok since the last "position" tag don't appeare above in the hierarchy.
            velocity
        subStation1
            axis1           // this is not ok since axis 1 appears above in the hierarchy !
                position
                velocity
            axis2
                position    // this is ok since there is no other 'position' in the parent objects
                velocity

