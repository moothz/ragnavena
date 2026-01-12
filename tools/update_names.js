const fs = require('fs');
const { execSync } = require('child_process');

const groupsFile = '/home/moothz/ragnavena/groups.json';
const targetNumbers = [
    '554187663096', '5491161796746', '12368659883', '5511952264969', '5511970478667',
    '5511983964998', '5511984405333', '5527996007606', '553499853478', '554298756604',
    '554398227079', '554699252174', '554797217020', '554899916578', '555581001228',
    '555596424307', '555596792072', '556984373902', '558186592176', '558188254009'
];

// DB Config
const MYSQL_CMD = 'mysql -u ragnarok -pBatataRagnavenaServerRoque ragnavena -N -e';

function sanitize(name) {
    // only letters and numbers, remove spaces, trim
    return name.replace(/[^a-zA-Z0-9]/g, '').trim();
}

function checkNameExists(name) {
    try {
        const query = "SELECT 1 FROM \\`char\\` WHERE name = '" + name + "'";
        const output = execSync(`${MYSQL_CMD} "${query}"`).toString().trim();
        return output === '1';
    } catch (e) {
        console.error(`Error checking name ${name}:`, e.message);
        return true; // Assume exists on error to be safe
    }
}

try {
    console.log('Reading groups.json...');
    const groupsData = fs.readFileSync(groupsFile, 'utf8');
    const groups = JSON.parse(groupsData);

    const numberToApelido = {};

    console.log('Parsing groups...');
    groups.forEach(group => {
        if (group.nicks && Array.isArray(group.nicks)) {
            group.nicks.forEach(nick => {
                if (nick.numero && nick.apelido) {
                    targetNumbers.forEach(target => {
                        if (nick.numero.startsWith(target)) {
                            numberToApelido[target] = nick.apelido;
                        }
                    });
                }
            });
        }
    });

    const sqlUpdates = [];
    
    console.log('Processing updates...');
    for (const number of targetNumbers) {
        if (numberToApelido[number]) {
            const oldName = `Player${number}`;
            let baseName = sanitize(numberToApelido[number]);
            
            // Initial length check
            if (baseName.length > 23) baseName = baseName.substring(0, 23);

            if (baseName.length < 4) {
                 console.log(`Skipping ${oldName} -> ${baseName} (too short)`);
                 continue;
            }

            let candidateName = baseName;
            let attempts = 0;
            let foundUnique = false;

            // Check if the current candidate name is ALREADY the name for this player (idempotency)
            // Or if the target player even exists.
            // But checking if "candidateName" is taken by *someone else* is the main goal.
            
            while (attempts < 5) {
                const exists = checkNameExists(candidateName);
                if (!exists) {
                    foundUnique = true;
                    break;
                } else {
                    // Check if it exists because it's ALREADY this user?
                    // We can check: SELECT char_id FROM char WHERE name = candidateName
                    // vs SELECT char_id FROM char WHERE name = oldName
                    // But simpler: just try to find a free name. 
                    // If the user already has this name, the UPDATE WHERE name='oldName' will just affect 0 rows, which is fine.
                    // BUT: If the user IS 'mutiz' (renamed previously) and we try to rename 'Player...' to 'mutiz', 
                    // 'mutiz' exists (it's him), so we might generate 'mutiz99'.
                    // So we must check if 'Player...' still exists first.
                    
                    const oldNameExists = checkNameExists(oldName);
                    if (!oldNameExists) {
                        console.log(`Player ${oldName} not found (maybe already renamed?). Skipping.`);
                        foundUnique = false; // Stop trying
                        break; 
                    }

                    console.log(`Name ${candidateName} is taken. Generating suffix...`);
                    const randomSuffix = Math.floor(Math.random() * 90 + 10); // 10-99
                    // Ensure space for suffix
                    const trimmedBase = baseName.substring(0, 21); 
                    candidateName = `${trimmedBase}${randomSuffix}`;
                    attempts++;
                }
            }

            if (foundUnique) {
                console.log(`Match: ${oldName} -> ${candidateName} (Original: ${numberToApelido[number]})`);
                sqlUpdates.push("UPDATE \`char\` SET name = '" + candidateName + "' WHERE name = '" + oldName + "';");
            } else if (attempts >= 5) {
                console.log(`Could not find unique name for ${oldName} (based on ${baseName}) after retries.`);
            }

        } else {
            console.log(`No nickname found for ${number}`);
        }
    }

    if (sqlUpdates.length > 0) {
        const sqlFile = '/home/moothz/ragnavena/update_names.sql';
        fs.writeFileSync(sqlFile, sqlUpdates.join('\n'));
        console.log(`Wrote ${sqlUpdates.length} updates to ${sqlFile}`);
        
        console.log('Executing SQL updates...');
        execSync(`mysql -u ragnarok -pBatataRagnavenaServerRoque ragnavena < ${sqlFile}`);
        console.log('Done.');
    } else {
        console.log('No updates to perform.');
    }

} catch (err) {
    console.error('Error:', err);
}