import { readGroups } from "./groups";

async function runWrapper() {
  try {
    const configGroups = await readGroups();
    console.log(
      `Found ${configGroups.length} group(s) in the local configuration file.`,
    );
  } catch (err) {
    console.error(`Failed to parse group configuration file: ${err}`);
    process.exit(1);
  }
}

runWrapper();
